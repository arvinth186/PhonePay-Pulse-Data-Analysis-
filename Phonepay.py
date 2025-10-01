import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import pymysql as mysql
import plotly.express as px
import requests
import json

# Database connection

conn = mysql.connect(
    host='127.0.0.1',
    user='root',
    password='root',
    database='phonepay'
)
cursor = conn.cursor()

# Aggegrated Insurance table data fetching

cursor.execute("select * from aggregated_insurance")
conn.commit()
table1=cursor.fetchall()

Aggre_insurance = pd.DataFrame(table1,columns=['States','Years','Quarter',
                                               'Name','Transaction_count','Transaction_amount'])

# Aggregated Transaction table data fetching
cursor.execute("select * from aggregated_transaction")
conn.commit()
table2=cursor.fetchall()

Aggre_transaction = pd.DataFrame(table2,columns=['States','Years','Quarter',
                                                 'Transaction_type','Transaction_count','Transaction_amount'])

# Aggregated User table data fetching
cursor.execute("select * from aggregated_user")
conn.commit()
table3=cursor.fetchall()

Aggre_user = pd.DataFrame(table3,columns=['States','Years','Quarter','Brand',
                                          'Transaction_count','Percentage'])

# Map Insurance table data fetching
cursor.execute("select * from map_insurance")
conn.commit()
table4=cursor.fetchall()

Map_insurance = pd.DataFrame(table4,columns=['States','Years','Quarter',
                                             'Districts','Transaction_count','Transaction_amount'])

# Map Transaction table data fetching
cursor.execute("select * from map_transaction")
conn.commit()
table5=cursor.fetchall()

Map_transaction = pd.DataFrame(table5,columns=['States','Years','Quarter',
                                               'Districts','Transaction_count','Transaction_amount'])

# Map User table data fetching
cursor.execute("select * from map_user")
conn.commit()
table6=cursor.fetchall()

Map_user = pd.DataFrame(table6,columns=['States','Years','Quarter',
                                        'Districts','RegisteredUsers','AppOpens'])

# Top Insurance table data fetching
cursor.execute("select * from top_insurance")
conn.commit()
table7=cursor.fetchall()

Top_insurance = pd.DataFrame(table7,columns=['States','Years','Quarter',
                                             'Pincodes','Transaction_count','Transaction_amount'])

# Top Transaction table data fetching
cursor.execute("select * from top_transaction")
conn.commit()
table8=cursor.fetchall()

Top_transaction = pd.DataFrame(table8,columns=['States','Years','Quarter',
                                               'Pincodes','Transaction_count','Transaction_amount'])

# Top User table data fetching
cursor.execute("select * from top_user")
conn.commit()
table9=cursor.fetchall()

Top_user = pd.DataFrame(table9,columns=['States','Years','Quarter',
                                        'Pincodes','RegisteredUsers'])



# ---------------------------------------------------------------------------------------------------------------------------#

 # ✅ Create human-readable format
def human_format(num):
        if num is None: 
            return None
        for unit in ['', 'K', 'M', 'B', 'T']:
            if abs(num) < 1000:
                return f"{num:.2f}{unit}"
            num /= 1000
        return f"{num:.2f}P"

# -----------------------------------------------------------------------------------------------------------------------------#
# Chart part components

# # Function for Yearly Transaction amount and count analysis for Insurance and Transaction table

def Transaction_amount_count_Y(df,year):
    tacy = df[df['Years']==year] 
    tacy.reset_index(drop=True,inplace=True)

    tacyg = tacy.groupby('States')[['Transaction_count','Transaction_amount']].sum()
    tacyg.reset_index(inplace=True)


    col1,col2=st.columns(2)

    with col1:
        # Bar chart for transaction_Amount column

        fig_amount = px.bar(tacyg,x='States',y='Transaction_amount',title=f'{year} Transaction Amount',
                            color_discrete_sequence=px.colors.sequential.Viridis)
        st.plotly_chart(fig_amount)


    with col2:
        # Bar chart for transaction_Count column

        fig_count = px.bar(tacyg,x='States',y='Transaction_count',title=f'{year} Transaction Count',
                           color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_count)



    # Loading GeoJSON data for India states througth URL
    
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

    response = requests.get(url)
    states_name=[]
    data1=json.loads(response.content)

    for feature in data1['features']:
        states_name.append(feature['properties']['ST_NM'])

    states_name.sort()

    col1,col2=st.columns(2)

    # Map for transaction_Amount column
    with col1:
        fig_india_amount = px.choropleth(tacyg,geojson=data1,locations='States',color='Transaction_amount',
                                        featureidkey='properties.ST_NM',title=f'{year} Transaction Amount by State',
                                        range_color=(tacyg['Transaction_amount'].min(),tacyg['Transaction_amount'].max()),
                                        color_continuous_scale='Viridis',fitbounds='locations',projection='mercator')
        
        fig_india_amount.update_geos(visible=False)
        fig_india_amount.update_layout(dragmode=False)
        st.plotly_chart(fig_india_amount)

    # Map for transaction_Count column
    with col2:
        fig_india_count = px.choropleth(tacyg,geojson=data1,locations='States',color='Transaction_count',
                                        featureidkey='properties.ST_NM',title=f'{year} Transaction Count by State',
                                        range_color=(tacyg['Transaction_count'].min(),tacyg['Transaction_count'].max()),
                                        color_continuous_scale='Bluered_r',fitbounds='locations',projection='mercator')

        fig_india_count.update_geos(visible=False)
        fig_india_count.update_layout(dragmode=False)
        st.plotly_chart(fig_india_count)


    return tacy


# ---------------------------------------------------------------------------------------------------------------------------#



# Function for Quarterly Transaction amount and count analysis for Insurance and Transaction table

# Bar chart for Quarterly Transaction amount and count

def Transaction_amount_count_Y_Q(df,quarter):

    tacy = df[df['Quarter']==quarter] 
    tacy.reset_index(drop=True,inplace=True)

    tacyg = tacy.groupby('States')[['Transaction_count','Transaction_amount']].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)

    with col1:
        # Bar chart for transaction_Amount column Quarterly

        fig_amount = px.bar(tacyg,x='States',y='Transaction_amount',title=f'{tacy['Years'].unique()} Years {quarter} Quarter Transaction Amount',
                            color_discrete_sequence=px.colors.sequential.Viridis)
        st.plotly_chart(fig_amount)

    with col2:
        # Bar chart for transaction_Count column Quarterly

        fig_count = px.bar(tacyg,x='States',y='Transaction_count',title=f'{tacy['Years'].unique()} Years {quarter} Quarter Transaction Count',
                           color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_count)
        



    # Map for transaction_Amount and Count column

    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

    response = requests.get(url)
    states_name=[]
    data1=json.loads(response.content)

    for feature in data1['features']:
        states_name.append(feature['properties']['ST_NM'])

    states_name.sort()

    col1,col2=st.columns(2)

    with col1:
        # Map for transaction_Amount column Quarterly

        fig_india_amount = px.choropleth(tacyg,geojson=data1,locations='States',color='Transaction_amount',
                                        featureidkey='properties.ST_NM',title=f'{tacy['Years'].unique()} Years {quarter} Quarter Transaction Amount by State',
                                        range_color=(tacyg['Transaction_amount'].min(),tacyg['Transaction_amount'].max()),
                                        color_continuous_scale='Viridis',fitbounds='locations',projection='mercator')
        
        fig_india_amount.update_geos(visible=False)
        fig_india_amount.update_layout(dragmode=False)
        st.plotly_chart(fig_india_amount)

    with col2:
        # Map for transaction_Count column Quarterly

        fig_india_count = px.choropleth(tacyg,geojson=data1,locations='States',color='Transaction_count',
                                         featureidkey='properties.ST_NM',title=f'{tacy['Years'].unique()} Years {quarter} Quarter Transaction Count by State',
                                         range_color=(tacyg['Transaction_count'].min(),tacyg['Transaction_count'].max()),
                                         color_continuous_scale='Rainbow',fitbounds='locations',projection='mercator')

        fig_india_count.update_geos(visible=False)
        fig_india_count.update_layout(dragmode=False)
        st.plotly_chart(fig_india_count)

    return tacy


#---------------------------------------------------------------------------------------------------------------------------#

# Function for Statewise Transaction amount and count analysis for unique transaction type

# Analysis of Transaction_count and Transaction_amount by Transaction_type for a State

def Aggre_Transaction_Type(df,state):

    tacy = df[df['States']== state]
    tacy.reset_index(drop=True,inplace=True)

    tacyg = tacy.groupby('Transaction_type')[['Transaction_count','Transaction_amount']].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)

    with col1:
        fig_pie_1 = px.pie(data_frame=tacyg,names='Transaction_type',values='Transaction_amount',
                        width=600,title=f"Transaction Amount for {state}",hole=0.5)

        st.plotly_chart(fig_pie_1)

    with col2:
        fig_pie_2 = px.pie(data_frame=tacyg,names='Transaction_type',values='Transaction_count',
                        width=600,title=f"Transaction Count for {state}",hole=0.5)

        st.plotly_chart(fig_pie_2)


# ---------------------------------------------------------------------------------------------------------------------------#

# Aggregated User table data fetching brands by year

def Aggre_user_brand_y(df,year):
    aguy=df[df['Years']==year]
    aguy.reset_index(drop=True,inplace=True)

    aguyg =pd.DataFrame(aguy.groupby('Brand')['Transaction_count'].sum())
    aguyg.reset_index(inplace=True)

    fig_bar_1 = px.bar(aguyg,x='Brand',y='Transaction_count',title=f'{year} Transaction Count by Brand',
                    color_discrete_sequence=px.colors.sequential.haline_r)
    st.plotly_chart(fig_bar_1)  

    return aguy

# ---------------------------------------------------------------------------------------------------------------------------#

# Aggregated User table data fetching by year and quarter
# aguyq -> Aggregated User Year Quarter

def Aggre_user_brand_Y_Q(df,Quarter):
    
    aguyq =df[df['Quarter']==Quarter]
    aguyq.reset_index(drop=True,inplace=True)

    aguyqg =pd.DataFrame(aguyq.groupby('Brand')['Transaction_count'].sum())
    aguyqg.reset_index(inplace=True)

    fig_bar_1 = px.bar(aguyqg,x='Brand',y='Transaction_count',title=f'{Quarter} Quarter Transaction Count by Brand',
                    color_discrete_sequence=px.colors.sequential.haline_r)
    
    st.plotly_chart(fig_bar_1)

    return aguyq


# ---------------------------------------------------------------------------------------------------------------------------#    

# Aggregated User table data fetching by State for the selected Year and Quarter
# aguyqs -> Aggregated User Year Quarter State

def Aggre_user_brand_y_q_state(df,state):

    aguyqs = df[df['States']==state]
    aguyqs.reset_index(drop=True,inplace=True)

    fig_line_1 = px.line(aguyqs,x='Brand',y='Transaction_count',title=f'{state} State Transaction Count by Brand',hover_data='Percentage',
                         color_discrete_sequence=px.colors.sequential.Plasma,markers=True)

    st.plotly_chart(fig_line_1) 

    return aguyqs



# ---------------------------------------------------------------------------------------------------------------------------#

# Analysis of Transaction_count and Transaction_amount by district for a State for Map Insurance table

def Map_insurance_district(df,state):

    tacy = df[df['States']== state]
    tacy.reset_index(drop=True,inplace=True)

    tacyg = tacy.groupby('Districts')[['Transaction_count','Transaction_amount']].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)

    with col1:
        fig_bar_1 = px.bar(data_frame=tacyg,x='Transaction_amount',y='Districts',
                        width=600,title=f"Transaction Amount for {state}",color_discrete_sequence=px.colors.sequential.Mint_r)

        st.plotly_chart(fig_bar_1)

    with col2:
        fig_bar_2 = px.bar(data_frame=tacyg,x='Transaction_count',y='Districts',
                        width=600,title=f"Transaction Count for {state}",color_discrete_sequence=px.colors.sequential.Mint_r)

        st.plotly_chart(fig_bar_2)


# ---------------------------------------------------------------------------------------------------------------------------#

# Analysis of  RegisteredUsers and AppOpens from Map_user table for the selected year

def Map_User_State_plot(df,year):
    muy=df[df['Years']==year]
    muy.reset_index(drop=True,inplace=True)

    muyg=muy.groupby('States')[['RegisteredUsers','AppOpens']].sum()
    muyg.reset_index(inplace=True)

    fig_line_1 = px.line(muyg,x='States',y=['RegisteredUsers','AppOpens'],title=f'{year} Registered Users and App Opens by States',markers=True,)

    st.plotly_chart(fig_line_1)
    return muy


#-------------------------------------------------------------------------------------------------------------------------------#

# Map_user table data fetching by quarter for RegisteredUsers and AppOpens for each state on the above selected year
def Map_User_State_plot_Y_Q(df,quarter):
    muyq=df[df['Quarter']==quarter]
    muyq.reset_index(drop=True,inplace=True)

    muyqg=muyq.groupby('States')[['RegisteredUsers','AppOpens']].sum()
    muyqg.reset_index(inplace=True)

    fig_line_1 = px.line(muyqg,x='States',y=['RegisteredUsers','AppOpens'],title=f'{quarter} Quarter Registered Users and App Opens by States',markers=True,)

    st.plotly_chart(fig_line_1)
    return muyq


#------------------------------------------------------------------------------------------------------------------------------#


# Analysis of state wise for the above selected quarter and year in map_user table
def Map_User_state_plot_Q(df,state):    
    muyqs =df[df['States']==state]
    muyqs.reset_index(drop=True,inplace=True)

    fig_map_user_bar_1 = px.bar(muyqs,x='RegisteredUsers',y='Districts',orientation='h',title=f'{state} Registered Users by Districts for {muyqs["Years"].unique()} Years {muyqs["Quarter"].unique()} Quarter',
                                color_discrete_sequence=px.colors.sequential.Plasma_r)
    st.plotly_chart(fig_map_user_bar_1)



    # fig_map_user_bar_2 = px.bar(muyqs,x='AppOpens',y='Districts',orientation='h',title=f'{state} App Opens by Districts for {muyqs["Years"].unique()} Years {muyqs["Quarter"].unique()} Quarter',
    #                             color_discrete_sequence=px.colors.sequential.Plasma_r)
    # st.plotly_chart(fig_map_user_bar_2)   

#---------------------------------------------------------------------------------------------------------------------------------#

# Analysis of Quarter wise for the selected year in Top_insurance table

def Top_insurance_amt_count_Y_Q(df,state):
    tiyq=df[df['States']==state]
    tiyq.reset_index(drop=True,inplace=True)

    col1,col2=st.columns(2)

    with col1:
        fig_amount = px.bar(tiyq,x='Quarter',y='Transaction_amount',title="Top Insurance Transaction Amount by Quarter for "+state,
                            color_discrete_sequence=px.colors.sequential.Viridis)

        st.plotly_chart(fig_amount)

    with col2:
        fig_count = px.bar(tiyq,x='Quarter',y='Transaction_count',title="Top Insurance Transaction Count by Quarter for "+state,
                            color_discrete_sequence=px.colors.sequential.Viridis)

        st.plotly_chart(fig_count)

# ---------------------------------------------------------------------------------------------------------------------------#
# Top_user table data fetching by year
# tuy -> Top User Year
# tuyg_s_q -> Top User Year Groupby States and Quarter

def Top_User_analysis_Y(df,year):
    tuy=df[df['Years']==year]
    tuy.reset_index(drop=True,inplace=True)

    tuyg_s_q=pd.DataFrame(tuy.groupby(['States','Quarter'])['RegisteredUsers'].sum())
    tuyg_s_q.reset_index(inplace=True)

    fig_top_plot_1=px.bar(tuyg_s_q,x='States',y='RegisteredUsers',color='Quarter', width=1000,height=600,
                          title=f'{year} Registered Users by States and Quarter',color_discrete_sequence=px.colors.sequential.Burgyl,
                          hover_name='States')
    
    st.plotly_chart(fig_top_plot_1)

    return tuy

#---------------------------------------------------------------------------------------------------------------------------#

# Top_user table data fetching by year and quarter
# tuys -> Top User Year Quarter

def Top_user_state_plot_Y(df,year):
    tuys=df[df['Years']==year]
    tuys.reset_index(drop=True,inplace=True)

    fig_top_plot_1=px.bar(tuys,x='Quarter',y='RegisteredUsers',color='Quarter',width=1000,height=600,
                            title=f'{year} Registered Users by States and Quarter',color_discrete_sequence=px.colors.sequential.Burgyl,
                            hover_data='Pincodes')
    
    st.plotly_chart(fig_top_plot_1)

    return tuys

# ---------------------------------------------------------------------------------------------------------------------------#

# yearly transaction_count_analysis
def yearly_transaction_count_analysis(year):
    cursor.execute(f"""select Years,States,sum(Transaction_count) as Yearly_Transaction_count
                   from aggregated_transaction
                   where Years={year}
                   group by Years,States
                   order by Years,Yearly_Transaction_count desc""")
    conn.commit()
    query = cursor.fetchall()
    query_df = pd.DataFrame(query,columns=['Years','States','Yearly_Transaction_count'])
    query_df['Yearly_Transaction_count_fmt'] =query_df['Yearly_Transaction_count'].apply(human_format)
    fig = px.bar(
                query_df.sort_values("Yearly_Transaction_count", ascending=True),  # sort for cleaner horizontal bars
                x="Yearly_Transaction_count",
                y="States",
                orientation="h",
                title=f"Yearly Transaction Count in Each State for the year {year}",
                text="Yearly_Transaction_count_fmt",  # show values on bars
                color="Yearly_Transaction_count",  # add gradient coloring
                color_continuous_scale="Blues"   # color scheme
            )
    st.plotly_chart(fig)
    return query_df

# ---------------------------------------------------------------------------------------------------------------------------#

#  Problem 1 query 3 uses aggregated_transaction table
def quarterly_transaction_count_analysis(year,quarter):
    cursor.execute(f"""select Years,States,sum(Transaction_count) as Quarterly_Transaction_count
                   from aggregated_transaction
                   where Years={year} and Quarter={quarter}
                   group by Years,States
                   order by Years,Quarterly_Transaction_count desc""")
    conn.commit()
    query = cursor.fetchall()
    query_df = pd.DataFrame(query,columns=['Years','States','Quarterly_Transaction_count'])
    query_df['Quarterly_Transaction_count_fmt'] =query_df['Quarterly_Transaction_count'].apply(human_format)
    fig = px.bar(
                query_df.sort_values("Quarterly_Transaction_count", ascending=True),  # sort for cleaner horizontal bars
                x="Quarterly_Transaction_count",
                y="States",
                orientation="h",
                title=f"Quarterly Transaction Count in Each State for the year {year} and quarter {quarter}",
                text="Quarterly_Transaction_count_fmt",  # show values on bars
                color="Quarterly_Transaction_count",  # add gradient coloring
                color_continuous_scale="Blues"   # color scheme
            )
    st.plotly_chart(fig)
    return query_df

#----------------------------------------------------------------------------------------------------------------------------#



# district wise transaction count analysis for the selected state for Problem 1
def district_wise_transaction_count(state):
    cursor.execute("""select Districts,States,sum(Transaction_count) as District_Transaction_count
                    from map_transaction
                    where States=%s 
                    group by Districts,States
                    order by District_Transaction_count desc""", (state,))
    conn.commit()
    query2 = cursor.fetchall()
    query2_df = pd.DataFrame(query2,columns=['Districts','States','District_Transaction_count'])
    query2_df['District_Transaction_count_fmt'] =query2_df['District_Transaction_count'].apply(human_format)
    # using heat map to visualize the data
    fig2 = px.bar(
                query2_df.sort_values("District_Transaction_count", ascending=True),  # sort for cleaner horizontal bars
                x="District_Transaction_count",
                y="Districts",
                orientation="h",
                title=f"District wise Transaction Count in {state}",
                text="District_Transaction_count_fmt",  # show values on bars
                color="District_Transaction_count",  # add gradient coloring
                color_continuous_scale="Blues"   # color scheme
            )
    st.plotly_chart(fig2)

# ---------------------------------------------------------------------------------------------------------------------------#    

# Analysis of Transaction_count and Transaction_amount by Transaction_type for Problem 1 query 3

def transaction_type_contribution():
    cursor.execute("""select Transaction_type, SUM(Transaction_amount) AS total_amount
                   from aggregated_transaction
                   group by Transaction_type
                   order by total_amount desc""")
    conn.commit()
    query = cursor.fetchall()
    query_df = pd.DataFrame(query,columns=['Transaction_type','total_amount'])
    query_df['total_amount_fmt'] = query_df['total_amount'].apply(human_format)
    col1,col2=st.columns(2)
    with col1:
        fig = px.bar(
                    query_df.sort_values("total_amount", ascending=True),  # sort for cleaner horizontal bars
                    x="total_amount",
                    y="Transaction_type",
                    orientation="h",
                    title=f"Total Transaction Amount by Type",
                    text="total_amount_fmt",  # show values on bars
                    color="total_amount",  # add gradient coloring
                    color_continuous_scale="Blues",   # color scheme
                    
                )
        st.plotly_chart(fig)

    with col2:
        fig2 = px.pie(
                    query_df,
                    names='Transaction_type',
                    values='total_amount',
                title='Percentage of Each Transaction Type to the Total Transaction Amount'
            )   
        st.plotly_chart(fig2)

    cursor.execute("""select Transaction_type, SUM(Transaction_count) AS total_count
                   from aggregated_transaction
                    group by Transaction_type
                    order by total_count desc""")
    conn.commit()
    query = cursor.fetchall()
    query_df = pd.DataFrame(query,columns=['Transaction_type','total_count'])
    query_df['total_count_fmt'] = query_df['total_count'].apply(human_format)
    
    col1,col2=st.columns(2)
    with col1:
        fig3 = px.bar(
                    query_df.sort_values("total_count", ascending=True),  # sort for cleaner horizontal bars
                    x="total_count",
                    y="Transaction_type",
                    orientation="h",
                    title=f"Total Transaction Count by Type",
                    text="total_count_fmt",  # show values on bars
                    color="total_count",  # add gradient coloring
                    color_continuous_scale="Blues"   # color scheme
                )
        st.plotly_chart(fig3)

    with col2:

        fig4 = px.pie(
                    query_df,
                    names='Transaction_type',
                    values='total_count',
                    title='Percentage of Each Transaction Type to the Total Transaction Count'
                )   
        st.plotly_chart(fig4)

    cursor.execute("""select Years,Transaction_type, SUM(Transaction_amount) AS total_amount
                   from aggregated_transaction
                     group by Years,Transaction_type
                        order by Years, total_amount desc""")
    conn.commit()
    query = cursor.fetchall()
    query_df = pd.DataFrame(query,columns=['Years','Transaction_type','total_amount'])
    query_df['total_amount_fmt'] = query_df['total_amount'].apply(human_format)

    col1,col2=st.columns(2)
    with col1:
        fig5 = px.line(
                    query_df,
                    x="Years",
                    y="total_amount",
                    color='Transaction_type',
                    title='Yearly Trend of Transaction Amount by Type'
                )
        st.plotly_chart(fig5)

    cursor.execute("""select Quarter,Transaction_type, SUM(Transaction_count) AS total_count
                   from aggregated_transaction
                     group by Quarter,Transaction_type
                        order by Quarter, total_count desc""")
    conn.commit()
    query = cursor.fetchall()
    query_df = pd.DataFrame(query,columns=['Quarter','Transaction_type','total_count'])
    with col2:
        fig6 = px.line(
                    query_df,
                    x="Quarter",
                    y="total_count",
                    color='Transaction_type',
                    title='Quarterly Trend of Transaction Count by Type'
                )
        st.plotly_chart(fig6)

# ---------------------------------------------------------------------------------------------------------------------------#

# Analysis of Transaction_count and Transaction_amount by Transaction_type for a selected year for Problem 1 query 3

def transaction_type_contribution_Y(year):

    cursor.execute(f"""select Years,Transaction_type, SUM(Transaction_amount) AS total_amount
                   from aggregated_transaction
                   where Years={year}
                     group by Years,Transaction_type
                        order by Years, total_amount desc""")
    conn.commit()
    query = cursor.fetchall()
    query_df = pd.DataFrame(query,columns=['Years','Transaction_type','total_amount'])
    query_df['total_amount_fmt'] = query_df['total_amount'].apply(human_format)
    col1,col2=st.columns(2)
    with col1:
        fig = px.bar(
                    query_df.sort_values("total_amount", ascending=True),  # sort for cleaner horizontal bars
                    x="total_amount",
                    y="Transaction_type",
                    orientation="h",
                    title=f"Total Transaction Amount by Type for the year {year}",
                    text="total_amount_fmt",  # show values on bars
                    color="total_amount",  # add gradient coloring
                    color_continuous_scale="Blues"   # color scheme   

        )
        st.plotly_chart(fig)

    cursor.execute(f"""select Years,Transaction_type, SUM(Transaction_count) AS total_count
                   from aggregated_transaction
                     where Years={year}
                        group by Years,Transaction_type
                            order by Years, total_count desc""")
    conn.commit()
    query = cursor.fetchall()
    query_df = pd.DataFrame(query,columns=['Years','Transaction_type','total_count'])
    query_df['total_count_fmt'] = query_df['total_count'].apply(human_format)
    with col2:
        fig = px.bar(
                    query_df.sort_values("total_count", ascending=True),  # sort for cleaner horizontal bars
                    x="total_count",
                    y="Transaction_type",
                    orientation="h",
                    title=f"Total Transaction Count by Type for the year {year}",
                    text="total_count_fmt",  # show values on bars
                    color="total_count",  # add gradient coloring
                    color_continuous_scale="Blues"   # color scheme
        )
        st.plotly_chart(fig)

#--------------------------------------------------------------------------------------------------------------------------#

# Analysis of YoY growth and fastest growing state for Problem 1 query 4

def fastest_growing_state_yoy_growth():
    cursor.execute("""select Years, 
                   (SUM(Transaction_amount) - LAG(SUM(Transaction_amount)) OVER (ORDER BY Years)) / LAG(SUM(Transaction_amount)) OVER (ORDER BY Years) * 100 AS growth_percentage_amount
                   from aggregated_transaction
                   group by Years
                   order by Years""")
    conn.commit()
    query = cursor.fetchall()
    query_df = pd.DataFrame(query,columns=['Years','growth_percentage_amount'])

    col1,col2=st.columns(2)
    with col1:
        fig = px.bar(
                    query_df.sort_values("growth_percentage_amount", ascending=True),  # sort for cleaner horizontal bars
                    x="growth_percentage_amount",
                    y="Years",
                    orientation="h",
                    title=f"Yearly Growth Percentage of Transaction Amount",
                    text="growth_percentage_amount",  # show values on bars
                    color="growth_percentage_amount",  # add gradient coloring
                    color_continuous_scale="Blues"   # color scheme
                )
        
        st.plotly_chart(fig)


    # total transaction_amount for every year
    cursor.execute(""" Select Years,
                   sum(Transaction_amount) as Total_Trans_amt
                   from aggregated_transaction
                   group by Years
                   order by Years""")
    conn.commit()
    query = cursor.fetchall()
    query_df = pd.DataFrame(query,columns=['Years','Total_Trans_amt'])
    query_df['Total_Trans_amt_fmt'] = query_df['Total_Trans_amt'].apply(human_format)
    with col2:
        fig = px.bar(
                    query_df.sort_values("Total_Trans_amt", ascending=True),  # sort for cleaner horizontal bars
                    x="Total_Trans_amt",
                    y="Years",
                    orientation="h",
                    title=f"Yearly Growth of Transaction Amount",
                    text="Total_Trans_amt_fmt",  # show values on bars
                    color="Total_Trans_amt",  # add gradient coloring
                    color_continuous_scale="Blues"   # color scheme
                )

        st.plotly_chart(fig)

#-----------------------------------------------------------------------------------------------------------#--------------------#

# growth percentage of transaction amount for each state for Problem 1 query 4

def fastest_growing_state_yoy_growth_state(state):
    cursor.execute(f"""select States,Years,
                   round((SUM(Transaction_amount) - LAG(SUM(Transaction_amount)) OVER (PARTITION BY States ORDER BY Years)) / LAG(SUM(Transaction_amount)) OVER (PARTITION BY States ORDER BY Years) * 100, 2) AS growth_percentage_amount
                   from aggregated_transaction
                   where States='{state}'
                   group by States,Years
                   order by States,Years""")
    conn.commit()
    query = cursor.fetchall()
    query_df = pd.DataFrame(query,columns=['States','Years','growth_percentage_amount'])
    col1,col2=st.columns(2)
    with col1:
        fig = px.bar(
                    query_df.sort_values("growth_percentage_amount", ascending=True),  # sort for cleaner horizontal bars
                    x="growth_percentage_amount",
                    y="Years",
                    orientation="h",
                    title=f"Yearly Growth Percentage of Transaction Amount in {state}",
                    text="growth_percentage_amount",  # show values on bars
                    color="growth_percentage_amount",  # add gradient coloring
                    color_continuous_scale="Blues"   # color scheme
                )
        st.plotly_chart(fig)
    
    # total transaction_amount for every state
    cursor.execute(f""" Select States,Years,
                   sum(Transaction_amount) as Total_Trans_amt
                   from aggregated_transaction
                   where States='{state}'
                   group by States,Years
                   order by States,Years""")
    conn.commit()
    query = cursor.fetchall()
    query_df = pd.DataFrame(query,columns=['States','Years','Total_Trans_amt'])
    query_df['Total_Trans_amt_fmt'] = query_df['Total_Trans_amt'].apply(human_format) 
    with col2:
        fig = px.bar(
                    query_df.sort_values("Total_Trans_amt", ascending=True),  # sort for cleaner horizontal bars
                    x="Total_Trans_amt",
                    y="Years",
                    orientation="h",
                    title=f"Yearly Total Transaction Amount in {state}",
                    text="Total_Trans_amt_fmt",  # show values on bars
                    color="Total_Trans_amt",  # add gradient coloring
                    color_continuous_scale="Blues"   # color scheme
                )
        st.plotly_chart(fig)



#------------------------------------------------------------------------------------------------------------------------------#
# declining transaction amount states for Problem 1 query 5
# [Chandigarh,Manipur]

def declining_transaction_amount_states():
    cursor.execute(f"""WITH state_yearly AS (
    SELECT 
        States,
        Years,
        SUM(Transaction_amount) AS total_amt
    FROM aggregated_transaction
    GROUP BY States, Years
),
with_lag AS (
    SELECT 
        States,
        Years,
        total_amt,
        LAG(total_amt) OVER (PARTITION BY States ORDER BY Years) AS prev_amt
    FROM state_yearly
)
SELECT DISTINCT States
FROM with_lag
WHERE total_amt < prev_amt
ORDER BY States;""")
    conn.commit()
    query = cursor.fetchall()
    query_df = pd.DataFrame(query,columns=['States'])
    return query_df['States'].unique().tolist()




# declining transaction amount states yearwise for Problem 1 query 5 
def declining_transaction_amount_states_yearwise(state):
    cursor.execute(f""" select States,Years,sum(Transaction_amount) as Total_Transaction_amount
                   from aggregated_transaction
                   where States='{state}'
                   group by States,Years
                   order by Years""")
    conn.commit()
    query = cursor.fetchall()
    query_df = pd.DataFrame(query,columns=['States','Years','Total_Transaction_amount'])
     # Convert Decimal → float
    query_df['Total_Transaction_amount'] = query_df['Total_Transaction_amount'].astype(float)
    query_df['Amount_Billions'] = query_df['Total_Transaction_amount'] / 1e9  # Convert to billions
    
    col1,col2=st.columns(2)
    with col1:
        fig = px.line(
                    query_df,
                    x='Years',
                    y='Amount_Billions',
                    title=f'Transaction Amount Trend: {state}',
                    markers=True,
                    line_shape='linear'
                )
        st.plotly_chart(fig)

    cursor.execute(f""" select States,Years,sum(Transaction_amount) as Total_Transaction_count
                   from aggregated_transaction
                   where States='{state}'
                   group by States,Years
                   order by Years""")
    conn.commit()
    query = cursor.fetchall()
    query_df = pd.DataFrame(query,columns=['States','Years','Total_Transaction_count'])
        # Convert Decimal → float
    query_df['Total_Transaction_count'] = query_df['Total_Transaction_count'].astype(float)
    with col2:
        fig = px.line(
                    query_df,
                    x='Years',
                    y='Total_Transaction_count',
                    title=f'Transaction Count Trend: {state}',
                    markers=True,
                    line_shape='linear'
                )
        st.plotly_chart(fig)

# ---------------------------------------------------------------------------------------------------------------------------#
# Analysis of Registered Users by Brand for Problem 2 query 1
def registered_users_by_brand():
    cursor.execute("""select Brands, SUM(Transaction_count) AS total_registered_users
                   from aggregated_user
                   group by Brands
                   order by total_registered_users desc""")
    conn.commit()
    query = cursor.fetchall()
    query_df = pd.DataFrame(query,columns=['Brands','total_registered_users'])
    query_df['total_registered_users_fmt'] = query_df['total_registered_users'].apply(human_format)
    col1,col2=st.columns(2)
    with col1:
        fig = px.bar(
                    query_df.sort_values("total_registered_users", ascending=True),  # sort for cleaner horizontal bars
                    x="total_registered_users",
                    y="Brands",
                    orientation="h",
                    title=f"Total Registered Users by Brand",
                    text="total_registered_users_fmt",  # show values on bars
                    color="total_registered_users",  # add gradient coloring
                    color_continuous_scale="Blues"   # color scheme
                )
        st.plotly_chart(fig)
    with col2:
        fig2 = px.pie(
                    query_df.head(5),
                    names='Brands',
                    values='total_registered_users',
                    title='Percentage Contribution of Each Brand to the Total Registered Users (Top 5 Brands)'
                )
        st.plotly_chart(fig2)


    cursor.execute("""select Years,Brands, SUM(Transaction_count) AS total_registered_users
                   from aggregated_user
                   group by Years,Brands
                   order by Years, total_registered_users desc""")
    conn.commit()
    query = cursor.fetchall()
    query_df = pd.DataFrame(query,columns=['Years','Brands','total_registered_users'])
    fig3 = px.line(
                query_df,
                x="Years",
                y="total_registered_users",
                color='Brands',
                title='Yearly Trend of Registered Users by Brand'
            )
    st.plotly_chart(fig3)
    
# ---------------------------------------------------------------------------------------------------------------------------#
# Analysis of Registered Users by Brand for a selected year for Problem 2 query 1
# 4th we should show the YoY of selected brand

def registered_users_by_brand_YOY(brand):
    cursor.execute(f"""select Years,Brands, SUM(Transaction_count) AS total_registered_users
                   from aggregated_user
                   where Brands='{brand}'
                   group by Years,Brands
                   order by Years, total_registered_users desc""")
    conn.commit()
    query = cursor.fetchall()
    query_df = pd.DataFrame(query,columns=['Years','Brands','total_registered_users'])
    query_df['total_registered_users_fmt'] = query_df['total_registered_users'].apply(human_format)
    fig = px.bar(
                query_df.sort_values("total_registered_users", ascending=True),  # sort for cleaner horizontal bars
                x="total_registered_users",
                y="Years",
                orientation="h",
                title=f"Yearly Registered Users for the Brand {brand}",
                text="total_registered_users_fmt",  # show values on bars
                color="total_registered_users",  # add gradient coloring
                color_continuous_scale="Blues"   # color scheme
            )
    st.plotly_chart(fig)

# ---------------------------------------------------------------------------------------------------------------------------#
#problem 2 query 2
# Analysis of Most Engaged Brand with Highest Percentage for Problem 2 query 2

def most_engaged_brand_highest_percentage():
    cursor.execute("""select Brands, round(SUM(Percentage), 2) AS total_percentage
                   from aggregated_user
                   group by Brands
                   order by total_percentage desc""")
    conn.commit()
    query = cursor.fetchall()
    query_df = pd.DataFrame(query,columns=['Brands','total_percentage'])
    
    fig = px.bar(
                query_df.sort_values("total_percentage", ascending=True),  # sort for cleaner horizontal bars
                x="total_percentage",
                y="Brands",
                orientation="h",
                title=f"Overall Percentage of Each Brand ",
                text="total_percentage",  # show values on bars
                color="total_percentage",  # add gradient coloring
            )
    st.plotly_chart(fig)

def most_engaged_brand_highest_percentage_yearly(year):
    cursor.execute(f"""select Years,Brands, round(SUM(Percentage), 2) AS total_percentage
                   from aggregated_user
                   where Years={year}
                   group by Years,Brands
                   order by Years, total_percentage desc""")
    conn.commit()
    query = cursor.fetchall()
    query_df = pd.DataFrame(query,columns=['Years','Brands','total_percentage'])
    fig = px.bar(
                query_df.sort_values("total_percentage", ascending=True),  # sort for cleaner horizontal bars
                x="total_percentage",
                y="Brands",
                orientation="h",
                title=f"{year} Percentage of Each Brand ",
                text="total_percentage",  # show values on bars
                color="total_percentage",  # add gradient coloring
            )
    st.plotly_chart(fig)
    return query_df

def most_engaged_brand_highest_percentage_state(year,state):
    cursor.execute(f"""select States,Years,Brands, round(SUM(Percentage), 2) AS total_percentage
                   from aggregated_user
                   where Years={year} and States='{state}'
                   group by States,Years,Brands
                   order by States,Years, total_percentage desc""")
    conn.commit()
    query = cursor.fetchall()
    query_df = pd.DataFrame(query,columns=['States','Years','Brands','total_percentage'])
    fig = px.bar(
                query_df.sort_values("total_percentage", ascending=True),  # sort for cleaner horizontal bars
                x="total_percentage",
                y="Brands",
                orientation="h",
                title=f"State wise Percentage  for the year {year}",
                text="total_percentage",  # show values on bars
                color="total_percentage",  # add gradient coloring
            )
    st.plotly_chart(fig)

# ---------------------------------------------------------------------------------------------------------------------------#
# problem 2 query 3
# Analysis of Most Engaged Brand with Highest Percentage for a selected year and quarter for Problem

def brand_share_by_state():
    cursor.execute("""select Brands, round(SUM(Percentage), 2) AS total_percentage
                   from aggregated_user
                   group by Brands
                   order by total_percentage desc""")
    conn.commit()
    query = cursor.fetchall()
    query_df = pd.DataFrame(query,columns=['Brands','total_percentage'])
    fig = px.bar(
                query_df.sort_values("total_percentage", ascending=True),  # sort for cleaner horizontal bars
                x="total_percentage",
                y="Brands",
                orientation="h",
                title=f"Overall Percentage of Each Brand ",
                text="total_percentage",  # show values on bars
                color="total_percentage",  # add gradient coloring
            )
    st.plotly_chart(fig)

    cursor.execute("""select Years,Brands, round(SUM(Percentage), 2) AS total_percentage
                   from aggregated_user
                   group by Years,Brands
                   order by Years, total_percentage desc""")
    conn.commit()
    query = cursor.fetchall()
    query_df = pd.DataFrame(query,columns=['Years','Brands','total_percentage'])
    fig = px.line(
                query_df,
                x="Years",
                y="total_percentage",
                color='Brands',
                title='Yearly Trend of Percentage of Each Brand'
            )
    st.plotly_chart(fig)

# ---------------------------------------------------------------------------------------------------------------------------#
# problem 2 query 4
# # Top device in each quarter for a selected year for Problem 2 query 4

def top_device_in_each_quarter_year(year):
    cursor.execute(f"""select Years,Quarter,Brands, SUM(Transaction_count) AS Transaction_count
                   from aggregated_user
                   where Years={year}
                   group by Years,Quarter,Brands
                   order by Years,Quarter, Transaction_count desc""")
    conn.commit()
    query = cursor.fetchall()
    query_df = pd.DataFrame(query,columns=['Years','Quarter','Brands','Transaction_count'])
    query_df['Transaction_count_fmt'] = query_df['Transaction_count'].apply(human_format)
    col1,col2=st.columns(2)
    with col1:
        fig = px.bar(
                    query_df.sort_values("Transaction_count", ascending=True),  # sort for cleaner horizontal bars
                    x="Transaction_count",
                    y="Brands",
                    orientation="h",
                    title=f"Top Device in Each Quarter for the year {year}",
                    text="Transaction_count_fmt",  # show values on bars
                    color="Transaction_count",  # add gradient coloring
                )
        st.plotly_chart(fig)

    # top 5 brands
    top_5_brands = query_df['Brands'].value_counts().nlargest(5).index
    top_5_df = query_df[query_df['Brands'].isin(top_5_brands)]
    with col2:
        fig2 = px.bar(
                    top_5_df.sort_values("Transaction_count", ascending=True),
                    x="Transaction_count",
                    y="Brands",
                    orientation="h",
                    title=f"Top 5 Devices in Each Quarter for the year {year}",
                    text="Transaction_count_fmt",  # show values on bars
                    color="Transaction_count",
                )
        st.plotly_chart(fig2)
    return query_df

def top_device_in_given_quarter(year, quarter):
        cursor.execute(f"""select Years,Quarter,Brands, SUM(Transaction_count) AS Transaction_count
                    from aggregated_user
                    where Years={year} and Quarter={quarter}
                    group by Years,Quarter,Brands
                    order by Years,Quarter, Transaction_count desc""")
        conn.commit()
        query = cursor.fetchall()
        query_df = pd.DataFrame(query,columns=['Years','Quarter','Brands','Transaction_count'])
        query_df['Transaction_count_fmt'] = query_df['Transaction_count'].apply(human_format)
        col1,col2=st.columns(2)
        with col1:
            fig = px.bar(
                        query_df.sort_values("Transaction_count", ascending=True),  # sort for cleaner horizontal bars
                        x="Transaction_count",
                        y="Brands",
                        orientation="h",
                        title=f"Top Device in {quarter} Quarter",
                        text="Transaction_count_fmt",  # show values on bars
                        color="Transaction_count",  # add gradient coloring
                    )
            st.plotly_chart(fig)
        # top 5 brands
        top_5_brands = query_df['Brands'].value_counts().nlargest(5).index
        top_5_df = query_df[query_df['Brands'].isin(top_5_brands)]
        with col2:
            fig2 = px.bar(
                        top_5_df.sort_values("Transaction_count", ascending=True),
                        x="Transaction_count",
                        y="Brands",
                        orientation="h",
                        title=f"Top 5 Devices in {quarter} Quarter for the year {year}",
                        text="Transaction_count_fmt",  # show values on bars
                        color="Transaction_count",
                    )
            st.plotly_chart(fig2)

# ---------------------------------------------------------------------------------------------------------------------------#

# problem 2 query 5
# Underutilized Devices for Problem 2 query 5
def underutilized_devices():
    cursor.execute(f""" select Brands,sum(Transaction_count) as registered_users,
                   round(avg(Percentage)*100,2) as avg_useage
                   from aggregated_user
                   group by brands
                   having avg_useage <5""")
    conn.commit()
    query=cursor.fetchall()
    query_df=pd.DataFrame(query,columns=['Brands','registered_users','avg_useage'])
    fig=px.bar(
                query_df.sort_values("avg_useage", ascending=True),  # sort for cleaner horizontal bars
                x="avg_useage",
                y="Brands",
                orientation="h",
                title=f"Underutilized Devices (Average Usage < 5%)",
                text="avg_useage",  # show values on bars
                color="avg_useage",  # add gradient coloring
            )
    st.plotly_chart(fig)

# ---------------------------------------------------------------------------------------------------------------------------#
# Problem 3 query 1
# State-wise insurance penetration

def state_wise_insurance_penetration():
    cursor.execute(f""" select States,sum(Insurance_count) as Total_Insurance_count,
                     sum(TotalIns_amount) as Total_Insurance_amount
                     from aggregated_insurance
                     group by States
                     order by Total_Insurance_count desc""")
    conn.commit()
    query=cursor.fetchall()

    col1,col2=st.columns(2)
    State_wise_insurance = pd.DataFrame(query,columns=['States','Total_Insurance_count','Total_Insurance_amount'])
    # Convert numeric columns to correct dtype
    State_wise_insurance['Total_Insurance_count'] = pd.to_numeric(State_wise_insurance['Total_Insurance_count'], errors='coerce')
    State_wise_insurance['Total_Insurance_amount'] = pd.to_numeric(State_wise_insurance['Total_Insurance_amount'], errors='coerce')
    with col1:
        fig1 = px.bar(
                    State_wise_insurance.sort_values("Total_Insurance_count", ascending=True),  # sort for cleaner horizontal bars
                    x="Total_Insurance_count",
                    y="States",
                    orientation="h",
                    title='State Wise Insurance Count',
                    color_discrete_sequence=px.colors.sequential.Viridis
        )
        st.plotly_chart(fig1)
    with col2:
        fig2 = px.bar(
                    State_wise_insurance.sort_values("Total_Insurance_amount", ascending=True),  # sort for cleaner horizontal bars
                    x="Total_Insurance_amount",
                    y="States",
                    orientation="h",
                    title='State Wise Insurance Amount',
                    color_discrete_sequence=px.colors.sequential.Viridis
        )
        st.plotly_chart(fig2)

    # Top 5 high and low insurance amount states

    col1,col2=st.columns(2)
    
    top_5_high_amount = State_wise_insurance.nlargest(5, 'Total_Insurance_amount')
    top_5_low_amount = State_wise_insurance.nsmallest(5, 'Total_Insurance_amount')
    with col1:
        fig3 = px.bar(top_5_high_amount,x='States',y='Total_Insurance_amount',title='Top 5 States by Insurance Amount',
                      color_discrete_sequence=px.colors.sequential.Viridis)
        st.plotly_chart(fig3)

    with col2:
        fig4 = px.bar(top_5_low_amount,x='States',y='Total_Insurance_amount',title='Bottom 5 States by Insurance Amount',
                      color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig4)

    # Top 5 high and low insurance count states
    top_5_high_count = State_wise_insurance.nlargest(5, 'Total_Insurance_count')
    top_5_low_count = State_wise_insurance.nsmallest(5, 'Total_Insurance_count')
    col1,col2=st.columns(2)
    with col1:
        fig5 = px.bar(top_5_high_count,x='States',y='Total_Insurance_count',title='Top 5 States by Insurance Count',
                      color_discrete_sequence=px.colors.sequential.Viridis)
        st.plotly_chart(fig5)

    with col2:
        fig6 = px.bar(top_5_low_count,x='States',y='Total_Insurance_count',title='Bottom 5 States by Insurance Count',
                      color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig6)

# ---------------------------------------------------------------------------------------------------------------------------#
# Problem 3 query 2
# Yearly insurance penetration

# problem 3 query 2
# Quarterly growth trend
# 1st we should should show the year wise growth on transaction amount and count for selected state using bar chart
# 2nd we should show the quarter wise growth on transaction amount and count for selected state using bar chart
# 3rd we should show the quarterly trend of transaction amount and count for selected state using line chart

def quarterly_growth_trend_state(state):
    cursor.execute(f""" select Years, sum(TotalIns_amount) as Total_Insurance_amount,
                   (sum(TotalIns_amount) - LAG(sum(TotalIns_amount)) OVER (ORDER BY Years)) / LAG(sum(TotalIns_amount)) OVER (ORDER BY Years) * 100 AS growth_percentage_amount
                   from aggregated_insurance
                   where States='{state}'
                   group by Years
                   order by Years""")
    conn.commit()
    query=cursor.fetchall()
    query_df=pd.DataFrame(query,columns=['Years','Total_Insurance_amount','growth_percentage_amount'])
    col1,col2=st.columns(2)
    
    with col1:
        fig1 = px.bar(
                    query_df.sort_values("growth_percentage_amount", ascending=True),  # sort for cleaner horizontal bars
                    x="growth_percentage_amount",
                    y="Years",
                    orientation="h",
                    title=f'Yearly Growth Percentage of Insurance Amount in {state}',
                    text="growth_percentage_amount",  # show values on bars
                    color="growth_percentage_amount",  # add gradient coloring
                )
        st.plotly_chart(fig1)
    query_df['Total_Insurance_amount_fmt'] = query_df['Total_Insurance_amount'].apply(human_format)
    with col2:
        fig2 = px.bar(
                query_df.sort_values("Total_Insurance_amount", ascending=True),  # sort for cleaner horizontal bars
                x="Total_Insurance_amount",
                y="Years",
                orientation="h",
                title=f'Yearly Total Insurance Amount in {state}',
                text="Total_Insurance_amount_fmt",  # show values on bars
                color="Total_Insurance_amount",  # add gradient coloring
            )
        st.plotly_chart(fig2)

    cursor.execute(f""" select Quarter, sum(TotalIns_amount) as Total_Insurance_amount,
                   (sum(TotalIns_amount) - LAG(sum(TotalIns_amount)) OVER (ORDER BY Quarter)) / LAG(sum(TotalIns_amount)) OVER (ORDER BY Quarter) * 100 AS growth_percentage_amount
                   from aggregated_insurance
                   where States='{state}'
                   group by Quarter
                   order by Quarter""")
    conn.commit()
    query=cursor.fetchall()
    query_df=pd.DataFrame(query,columns=['Quarter','Total_Insurance_amount','growth_percentage_amount'])
    fig3 = px.bar(
                query_df.sort_values("growth_percentage_amount", ascending=True),  # sort for cleaner horizontal bars
                x="growth_percentage_amount",
                y="Quarter",
                orientation="h",
                title=f'Quarterly Growth Percentage of Insurance Amount in {state}',
                text="growth_percentage_amount",  # show
                color="growth_percentage_amount"
    )
    st.plotly_chart(fig3)

# -----------------------------------------------------------------------------------------------------------#
# Problem 3 query 3
# States with highest penetration (average premium)
def states_with_highest_penetration():
    cursor.execute(f""" select States,round(SUM(TotalIns_amount)/SUM(Insurance_count),2) AS avg_premium
                   FROM aggregated_insurance
                   GROUP BY States
                   ORDER BY avg_premium DESC""")
    conn.commit()
    query=cursor.fetchall()
    query_df=pd.DataFrame(query,columns=['States','avg_premium'])
    fig = px.bar(
                query_df.sort_values("avg_premium", ascending=True),  # sort for cleaner horizontal bars
                x="avg_premium",
                y="States",
                orientation="h",
                title=f"States with Highest Penetration (Average Premium)",
                text="avg_premium",  # show values on bars
                color="avg_premium",  # add gradient coloring
            )
    st.plotly_chart(fig)

# ---------------------------------------------------------------------------------------------------------------------------#
# Problem 3 query 4

# problem 3 query 4
# Fastest growing state

def fastest_growing_state():
    cursor.execute(f""" select Years, 
                   (SUM(TotalIns_amount) - LAG(SUM(TotalIns_amount)) OVER (ORDER BY Years)) / LAG(SUM(TotalIns_amount)) OVER (ORDER BY Years) * 100 AS growth_percentage_amount
                   from aggregated_insurance
                   group by Years
                   order by Years""")
    conn.commit()
    query=cursor.fetchall()
    query_df=pd.DataFrame(query,columns=['Years','growth_percentage_amount'])
    fig = px.bar(
                query_df.sort_values("growth_percentage_amount", ascending=True),  # sort for cleaner horizontal bars
                x="growth_percentage_amount",
                y="Years",
                orientation="h",
                title=f"Yearly Growth Percentage of Insurance Amount",
                text="growth_percentage_amount",  # show values on bars
                color="growth_percentage_amount",  # add gradient coloring
            )
    st.plotly_chart(fig)
    return query_df

def fastest_growing_state_selected(state):
    cursor.execute(f""" select States,Years,
                   (SUM(TotalIns_amount) - LAG(SUM(TotalIns_amount)) OVER (PARTITION BY States ORDER BY Years)) / LAG(SUM(TotalIns_amount)) OVER (PARTITION BY States ORDER BY Years) * 100 AS growth_percentage_amount
                   from aggregated_insurance
                   where States='{state}'
                   group by States,Years
                   order by States,Years""")
    conn.commit()
    query=cursor.fetchall()
    query_df=pd.DataFrame(query,columns=['States','Years','growth_percentage_amount'])
    fig = px.bar(
                query_df.sort_values("growth_percentage_amount", ascending=True),  # sort for cleaner horizontal bars
                x="growth_percentage_amount",
                y="Years",
                orientation="h",
                title=f"Yearly Growth Percentage of Insurance Amount in {state}",
                text="growth_percentage_amount",  # show values on bars
                color="growth_percentage_amount",  # add gradient coloring
            )
    st.plotly_chart(fig)

# ---------------------------------------------------------------------------------------------------------------------------#  

# problem 3 query 5
# Untapped states (low insurance count)
def untapped_states_low_insurance_count():
    cursor.execute(f""" select States,sum(Insurance_count) as Total_Insurance_count
                   from aggregated_insurance
                   group by States
                   having Total_Insurance_count < 50000
                   order by Total_Insurance_count""")
    conn.commit()
    query=cursor.fetchall()
    query_df=pd.DataFrame(query,columns=['States','Total_Insurance_count'])
    fig = px.bar(
                query_df.sort_values("Total_Insurance_count", ascending=True),  # sort for cleaner horizontal bars
                x="Total_Insurance_count",
                y="States",
                orientation="h",
                title=f"Untapped States (Low Insurance Count < 50,000)",
                text="Total_Insurance_count",  # show values on bars
                color="Total_Insurance_count",  # add gradient coloring
            )
    st.plotly_chart(fig)

# ---------------------------------------------------------------------------------------------------------------------------#

# problem 4 query 1
# State contribution share



def state_contribution_share():
    cursor.execute(f""" select States, SUM(Transaction_amount) AS total_amt,
                   SUM(Transaction_amount) * 100 / sum(sum(Transaction_amount)) over() percent_share
                   FROM aggregated_transaction
                   GROUP BY States
                   order by total_amt desc""")
    conn.commit()
    query=cursor.fetchall()
    query_df=pd.DataFrame(query,columns=['States','total_amt','percent_share'])
    fig = px.bar(
                query_df.sort_values("percent_share", ascending=True),  # sort for cleaner horizontal bars
                x="percent_share",
                y="States",
                orientation="h",
                title=f"State Contribution Share",
                text="percent_share",  # show values on bars
                color="percent_share",  # add gradient coloring
            )
    st.plotly_chart(fig)
    query_df['percent_share'] = pd.to_numeric(query_df['percent_share'],errors='coerce')
    top_5_states = query_df.nlargest(5, 'percent_share')
    col1,col2=st.columns(2)
    with col1:
        fig2 = px.bar(top_5_states,x='States',y='percent_share',title='Top 5 States by Contribution Share',
                    color_discrete_sequence=px.colors.sequential.Viridis)
        st.plotly_chart(fig2)
    with col2:
        bottom_5_states = query_df.nsmallest(5, 'percent_share')
        fig3 = px.bar(bottom_5_states,x='States',y='percent_share',title='Bottom 5 States by Contribution Share',
                    color_discrete_sequence=px.colors.sequential.Bluered_r) 
        st.plotly_chart(fig3)

# ---------------------------------------------------------------------------------------------------------------------------#
# problem 4 query 2
# Districts with highest transaction count

def districts_with_highest_transaction_count(state):
    cursor.execute(f""" select States,Districts, SUM(Transaction_count) AS total_transaction_count
                   from map_transaction
                   where States='{state}'
                   group by Districts,States
                   order by total_transaction_count desc""")
    conn.commit()
    query=cursor.fetchall()
    
    query_df=pd.DataFrame(query,columns=['States','Districts','total_transaction_count'])
    query_df['total_transaction_count'] = pd.to_numeric(query_df['total_transaction_count'],errors='coerce')
    query_df['total_transaction_count_fmt'] = query_df['total_transaction_count'].apply(human_format)
    
    
    fig = px.bar(
                query_df.sort_values("total_transaction_count", ascending=True),  # sort for cleaner horizontal bars
                x="total_transaction_count",
                y="Districts",
                orientation="h",
                title=f"Districts with Highest Transaction Count on {state}",
                text="total_transaction_count_fmt",  # show values on bars
                color="total_transaction_count",  # add gradient coloring
            )
    st.plotly_chart(fig)
    col1,col2=st.columns(2)
    with col1:
        top_10_districts = query_df.nlargest(10, 'total_transaction_count')
        fig2 = px.bar(top_10_districts,x='Districts',y='total_transaction_count',title=f'Top 10 Districts by Transaction Count on {state}',
                      color_discrete_sequence=px.colors.sequential.Viridis)
        st.plotly_chart(fig2)
    with col2:
        bottom_10_districts = query_df.nsmallest(10, 'total_transaction_count')
        fig3 = px.bar(bottom_10_districts,x='Districts',y='total_transaction_count',title=f'Bottom 10 Districts by Transaction Count on {state}',
                    color_discrete_sequence=px.colors.sequential.Bluered_r) 
        st.plotly_chart(fig3)
    return query_df

def districts_with_highest_transaction_count_year(year,state):
    cursor.execute(f""" select States,Districts, SUM(Transaction_count) AS total_transaction_count
                   from map_transaction
                   where Years={year} and States='{state}'
                   group by Districts,States
                   order by total_transaction_count desc""")
    conn.commit()
    query=cursor.fetchall()
    query_df=pd.DataFrame(query,columns=['States','Districts','total_transaction_count'])
    query_df['total_transaction_count'] = pd.to_numeric(query_df['total_transaction_count'],errors='coerce')
    query_df['total_transaction_count_fmt'] = query_df['total_transaction_count'].apply(human_format)
    
    fig = px.bar(
                query_df.sort_values("total_transaction_count", ascending=True),  # sort for cleaner horizontal bars
                x="total_transaction_count",
                y="Districts",
                orientation="h",
                title=f"Districts with Highest Transaction Count in {year}",
                text="total_transaction_count_fmt",  # show values on bars
                color="total_transaction_count",  # add gradient coloring
            )
    st.plotly_chart(fig)
    col1,col2=st.columns(2)
    with col1:
        top_10_districts = query_df.nlargest(10, 'total_transaction_count')
        fig2 = px.bar(top_10_districts,x='Districts',y='total_transaction_count',title=f'Top 10 Districts by Transaction Count in {year}',
                      color_discrete_sequence=px.colors.sequential.Viridis)
        st.plotly_chart(fig2)
    with col2:
        bottom_10_districts = query_df.nsmallest(10, 'total_transaction_count')
        fig3 = px.bar(bottom_10_districts,x='Districts',y='total_transaction_count',title=f'Bottom 10 Districts by Transaction Count in {year}',
                       color_discrete_sequence=px.colors.sequential.Bluered_r) 
        st.plotly_chart(fig3)

# ---------------------------------------------------------------------------------------------------------------------------#
# problem 4 query 3


def yearly_growth_rate():
    cursor.execute(f""" select Years, 
                   (SUM(Transaction_amount) - LAG(SUM(Transaction_amount)) OVER (ORDER BY Years)) / LAG(SUM(Transaction_amount)) OVER (ORDER BY Years) * 100 AS growth_percentage_amount
                   from aggregated_transaction
                   group by Years
                   order by Years""")
    conn.commit()
    query=cursor.fetchall()
    query_df=pd.DataFrame(query,columns=['Years','growth_percentage_amount'])
    fig = px.bar(
                query_df.sort_values("growth_percentage_amount", ascending=True),  # sort for cleaner horizontal bars
                x="growth_percentage_amount",
                y="Years",
                orientation="h",
                title=f"Yearly Growth Percentage of Transaction Amount",
                text="growth_percentage_amount",  # show values on bars
                color="growth_percentage_amount",  # add gradient coloring
            )
    st.plotly_chart(fig)
    # top 5 states
    cursor.execute(f""" select States,Years,
                   (SUM(Transaction_amount) - LAG(SUM(Transaction_amount)) OVER (PARTITION BY States ORDER BY Years)) / LAG(SUM(Transaction_amount)) OVER (PARTITION BY States ORDER BY Years) * 100 AS growth_percentage_amount
                   from aggregated_transaction
                   group by States,Years
                   order by States,Years""")
    conn.commit()
    query=cursor.fetchall()
    query_df=pd.DataFrame(query,columns=['States','Years','growth_percentage_amount'])
    query_df['growth_percentage_amount'] = pd.to_numeric(query_df['growth_percentage_amount'],errors='coerce')
    top_5_states = query_df.nlargest(5, 'growth_percentage_amount')     
    fig2 = px.bar(top_5_states,x='States',y='growth_percentage_amount',title='Top 5 States by Growth Percentage',
                  color_discrete_sequence=px.colors.sequential.Viridis)
    st.plotly_chart(fig2)
    return query_df 

def yearly_growth_rate_selected(state):
    cursor.execute(f""" select States,Years,
                   (SUM(Transaction_amount) - LAG(SUM(Transaction_amount)) OVER (PARTITION BY States ORDER BY Years)) / LAG(SUM(Transaction_amount)) OVER (PARTITION BY States ORDER BY Years) * 100 AS growth_percentage_amount
                   from aggregated_transaction
                   where States='{state}'
                   group by States,Years
                   order by States,Years""")
    conn.commit()
    query=cursor.fetchall()
    query_df=pd.DataFrame(query,columns=['States','Years','growth_percentage_amount'])
    fig = px.bar(
                query_df.sort_values("growth_percentage_amount", ascending=True),  # sort for cleaner horizontal bars
                x="growth_percentage_amount",
                y="Years",
                orientation="h",
                title=f"Yearly Growth Percentage of Transaction Amount in {state}",
                text="growth_percentage_amount",  # show values on bars
                color="growth_percentage_amount",  # add gradient coloring
            )
    st.plotly_chart(fig)

# ---------------------------------------------------------------------------------------------------------------------------#
# problem 4 query 4
# Quarter with peak transactions

def quarter_with_peak_transactions():
    cursor.execute(f""" select Quarter, SUM(Transaction_amount) AS total_transaction_amount
                   from aggregated_transaction
                   group by Quarter
                   order by total_transaction_amount desc""")
    conn.commit()
    query=cursor.fetchall()
    query_df=pd.DataFrame(query,columns=['Quarter','total_transaction_amount'])
    query_df['total_transaction_amount_fmt'] =query_df['total_transaction_amount'].apply(human_format)
    fig = px.bar(
                query_df.sort_values("total_transaction_amount", ascending=True),  # sort for cleaner horizontal bars
                x="total_transaction_amount",
                y="Quarter",
                orientation="h",
                title=f"Quarter with Peak Transactions",
                text="total_transaction_amount_fmt",  # show values on bars
                color="total_transaction_amount",  # add gradient coloring
            )
    st.plotly_chart(fig)
    return query_df

# state wise peak quarter
def quarter_with_peak_transactions_state(state):
    cursor.execute(f""" select States,Quarter, SUM(Transaction_amount) AS total_transaction_amount
                   from aggregated_transaction
                   where States='{state}'
                   group by States,Quarter
                   order by total_transaction_amount desc""")
    conn.commit()
    query=cursor.fetchall()
    query_df=pd.DataFrame(query,columns=['States','Quarter','total_transaction_amount'])
    query_df['total_transaction_amount_fmt'] =query_df['total_transaction_amount'].apply(human_format)
    fig = px.bar(
                query_df.sort_values("total_transaction_amount", ascending=True),  # sort for cleaner horizontal bars
                x="total_transaction_amount",
                y="Quarter",
                orientation="h",
                title=f"Quarter with Peak Transactions in {state}",
                text="total_transaction_amount_fmt",  # show values on bars
                color="total_transaction_amount",  # add gradient coloring
            )
    st.plotly_chart(fig)
    return query_df

# ---------------------------------------------------------------------------------------------------------------------------#

# problem 4 query 5
# Compare top vs bottom states

def compare_top_vs_bottom_states():
    cursor.execute(f""" select States, SUM(Transaction_amount) AS total_transaction_amount
                   from aggregated_transaction
                   group by States
                   order by total_transaction_amount desc""")
    conn.commit()
    query=cursor.fetchall()
    query_df=pd.DataFrame(query,columns=['States','total_transaction_amount'])
    query_df['total_transaction_amount'] = pd.to_numeric(query_df['total_transaction_amount'],errors='coerce')
    top_5_states = query_df.nlargest(5, 'total_transaction_amount')
    fig1 = px.bar(top_5_states,x='States',y='total_transaction_amount',title='Top 5 States by Transaction Amount',
                  color_discrete_sequence=px.colors.sequential.Viridis)
    st.plotly_chart(fig1)
    bottom_5_states = query_df.nsmallest(5, 'total_transaction_amount')
    fig2 = px.bar(bottom_5_states,x='States',y='total_transaction_amount',title='Bottom 5 States by Transaction Amount',
                    color_discrete_sequence=px.colors.sequential.Bluered_r) 
    st.plotly_chart(fig2)

# ---------------------------------------------------------------------------------------------------------------------------#

# problem 5 query 1

# problem 5 query 1
# Total registered users per state

def total_registered_users_per_state():
    cursor.execute(f""" select States, SUM(Registeredusers) AS total_registered_users
                   from map_user
                   group by States
                   order by total_registered_users desc""")
    conn.commit()
    query=cursor.fetchall()
    query_df=pd.DataFrame(query,columns=['States','total_registered_users'])
    query_df['total_registered_users_fmt']=query_df['total_registered_users'].apply(human_format)
    fig = px.bar(
                query_df.sort_values("total_registered_users", ascending=True),  # sort for cleaner horizontal bars
                x="total_registered_users",
                y="States",
                orientation="h",
                title=f"Total Registered Users per State",
                text="total_registered_users_fmt",  # show values on bars
                color="total_registered_users_fmt",  # add gradient coloring
            )
    st.plotly_chart(fig)
    return query_df

def total_registered_users_selected_state(state):
    cursor.execute(f"""select States,Years, SUM(Registeredusers) AS total_registered_users
                   from map_user
                   where States='{state}'
                   group by States,Years
                   order by total_registered_users desc""")
    conn.commit()
    query=cursor.fetchall()
    query_df=pd.DataFrame(query,columns=['States','Years','total_registered_users'])
    query_df['total_registered_users_fmt']=query_df['total_registered_users'].apply(human_format)
    query_df['color_fmt'] = query_df['total_registered_users'].apply(human_format)


    fig = px.bar(
                query_df.sort_values("total_registered_users", ascending=True),  # sort for cleaner horizontal bars
                x="total_registered_users",
                y="Years",
                orientation="h",
                title=f"Total Registered Users in {state}",
                text="total_registered_users_fmt",  # show values on bars
                color="color_fmt",  # add gradient coloring
                
            )
    st.plotly_chart(fig)
    return query_df

# ---------------------------------------------------------------------------------------------------------------------------#
# problem 5 query 2


def app_opens_vs_registered_users():
    cursor.execute(f""" select States, SUM(RegisteredUsers) AS users, SUM(AppOpens) AS opens,
                   SUM(AppOpens)/SUM(RegisteredUsers) AS engagement_ratio
                   FROM map_user
                   GROUP BY States
                   order by engagement_ratio desc""")
    conn.commit()
    query=cursor.fetchall()
    query_df=pd.DataFrame(query,columns=['States','users','opens','engagement_ratio'])
    fig = px.bar(
                query_df.sort_values("engagement_ratio", ascending=True),  # sort for cleaner horizontal bars
                x="engagement_ratio",
                y="States",
                orientation="h",
                title=f"App Opens vs Registered Users (Engagement Ratio)",
                text="engagement_ratio",  # show values on bars
                color="engagement_ratio",  # add gradient coloring
            )
    st.plotly_chart(fig)
    return query_df

def engagement_ratio_yearly_state(state):
    cursor.execute(f""" select States,Years, SUM(RegisteredUsers) AS users, SUM(AppOpens) AS opens,
                   SUM(AppOpens)/SUM(RegisteredUsers) AS engagement_ratio
                   FROM map_user
                   where States='{state}'
                   GROUP BY States,Years
                   order by engagement_ratio desc""")
    conn.commit()
    query=cursor.fetchall()
    query_df=pd.DataFrame(query,columns=['States','Years','users','opens','engagement_ratio'])
    fig = px.bar(
                query_df.sort_values("engagement_ratio", ascending=True),  # sort for cleaner horizontal bars
                x="engagement_ratio",
                y="Years",
                orientation="h",
                title=f"Engagement Ratio in {state}",
                text="engagement_ratio",  # show values on bars
                color="engagement_ratio",  # add gradient coloring
            )
    st.plotly_chart(fig)
    return query_df

# ---------------------------------------------------------------------------------------------------------------------------#
# problem 5 query 3
#  Districts with highest engagement

def overall_highest_engagement_district():
    cursor.execute(f""" select States,Districts, SUM(RegisteredUsers) AS users, SUM(AppOpens) AS opens,
                   SUM(AppOpens)/SUM(RegisteredUsers) AS engagement_ratio
                   FROM map_user
                   GROUP BY States,Districts
                   order by engagement_ratio desc""")
    conn.commit()
    query=cursor.fetchall()
    query_df=pd.DataFrame(query,columns=['States','Districts','users','opens','engagement_ratio'])
    # top 5 districts
    col1,col2=st.columns(2)
    query_df['engagement_ratio'] = pd.to_numeric(query_df['engagement_ratio'], errors='coerce')
    top_5_df = query_df.nlargest(5, 'engagement_ratio')
    with col1:
        fig = px.bar(
                    top_5_df.sort_values("engagement_ratio", ascending=True),  # sort for cleaner horizontal bars
                    x="engagement_ratio",
                    y="Districts",
                    orientation="h",
                    title=f"Districts with Highest Engagement Overall",
                    text="engagement_ratio",  # show values on bars
                    color="engagement_ratio",  # add gradient coloring
                )
        st.plotly_chart(fig)
    
    # bottom 5 districts
    bottom_5_df = query_df.nsmallest(5, 'engagement_ratio')
    with col2:
        fig2 = px.bar(
                    bottom_5_df.sort_values("engagement_ratio", ascending=True),  # sort for cleaner horizontal bars
                x="engagement_ratio",
                y="Districts",
                orientation="h",
                title=f"Districts with Lowest Engagement Overall",
                text="engagement_ratio",  # show values on bars
                color="engagement_ratio",  # add gradient coloring
            )       
        st.plotly_chart(fig2)

    return query_df


def districts_with_highest_engagement(state):
    cursor.execute(f""" select States,Districts, SUM(RegisteredUsers) AS users, SUM(AppOpens) AS opens,
                   SUM(AppOpens)/SUM(RegisteredUsers) AS engagement_ratio
                   FROM map_user
                   where States='{state}'
                   GROUP BY States,Districts
                   order by engagement_ratio desc""")
    conn.commit()
    query=cursor.fetchall()
    query_df=pd.DataFrame(query,columns=['States','Districts','users','opens','engagement_ratio'])
    # top 5 districts
    col1,col2=st.columns(2)
    query_df['engagement_ratio'] = pd.to_numeric(query_df['engagement_ratio'], errors='coerce')
    top_5_df = query_df.nlargest(5, 'engagement_ratio')
    with col1:
        fig = px.bar(
                    top_5_df.sort_values("engagement_ratio", ascending=True),  # sort for cleaner horizontal bars
                    x="engagement_ratio",
                y="Districts",
                orientation="h",
                title=f"Districts with Highest Engagement in {state}",
                text="engagement_ratio",  # show values on bars
                color="engagement_ratio",  # add gradient coloring
            )
        st.plotly_chart(fig)
    # bottom 5 districts
    bottom_5_df = query_df.nsmallest(5, 'engagement_ratio')
    with col2:
        fig2 = px.bar(
                    bottom_5_df.sort_values("engagement_ratio", ascending=True),  # sort for cleaner horizontal bars
                    x="engagement_ratio",
                y="Districts",
                orientation="h",
                title=f"Districts with Lowest Engagement in {state}",
                text="engagement_ratio",  # show values on bars
                color="engagement_ratio",  # add gradient coloring
            )       
        st.plotly_chart(fig2)

    return query_df

# ----------------------------------------------------------------------------------------------------------------------------#

# problem 5 query 4
# Growth trend over years
# 1st we shown the trend of given year for asked state
# 2nd we shown the trend of 2025-2027
from statsmodels.tsa.arima.model import ARIMA
import numpy as np

def growth_trend_over_years(state):
    cursor.execute(f""" select states,years,sum(RegisteredUsers) as total_usr
                   from map_user
                    where states='{state}'
                   group by states,years
                   order by states,years""")
    conn.commit()
    query=cursor.fetchall()
    query_df=pd.DataFrame(query,columns=['states','years','total_usr'])
    fig = px.line(query_df, x='years', y='total_usr', color='states', title='Growth Trend of Registered Users Over Years by State')
    st.plotly_chart(fig)
    return query_df


def forecast_trend_Regusers(state,forecast_years=3):

    cursor.execute(f"""  SELECT states, years, SUM(RegisteredUsers) AS total_usr
                            FROM map_user
                            WHERE states='{state}'
                            GROUP BY states, years
                            ORDER BY years
                        """)
    
    conn.commit()
    query=cursor.fetchall()
    query_df = pd.DataFrame(query,columns=['states','years','total_usr'])
    query_df['years'] = pd.to_numeric(query_df['years'], errors='coerce')
    query_df['total_usr'] = pd.to_numeric(query_df['total_usr'], errors='coerce')

    query_df['YoY_growth_pct']=query_df['total_usr'].pct_change()*100
    
    # forecast
    if forecast_years>0:
        series=query_df.set_index('years')['total_usr']
        series = series.astype(float)
        series.index = pd.PeriodIndex(series.index, freq='Y')
        model=ARIMA(series,order=(1,1,1))
        model_fit=model.fit()
        forecast=model_fit.forecast(steps=forecast_years)
        future_years=[query_df['years'].iloc[-1]+i for i in range(1,forecast_years+1)]
        forecast_df = pd.DataFrame({
            "states": state,
            "years": future_years,
            "total_usr": forecast,
            "YoY_growth_pct": np.nan  # can calculate vs last actual if needed
        })

        query_df = pd.concat([query_df, forecast_df], ignore_index=True)

        col1,col2=st.columns(2)
        with col1:
            fig = px.line(
                query_df,
                x='years',
                y='total_usr',
                color='states',
                markers=True,
                title=f'Growth Trend of Registered Users in {state}'
            )
            st.plotly_chart(fig)
        forecast_only = query_df[query_df['years'].isin(future_years)]
        forecast_only['total_usr_fmt']=forecast_only['total_usr'].apply(human_format)
        with col2:
            fig2 = px.bar(
                forecast_only,
                x='years',
                y='total_usr',
                color='states',
                text='total_usr_fmt',
                orientation='v',  # vertical bar is usually clearer for years
                title=f'Forecasted Registered Users in {state} (2025–2027)'
            )
            st.plotly_chart(fig2)

        return query_df

# ---------------------------------------------------------------------------------------------------------------------------#

# problem 5 query 5
#  Underperforming states (low app opens)

def underperforming_states_low_app_opens():
    cursor.execute(f""" select States, SUM(AppOpens) AS total_app_opens
                   from map_user
                   group by States
                   order by total_app_opens""")
    conn.commit()
    query=cursor.fetchall()
    query_df=pd.DataFrame(query,columns=['States','total_app_opens'])
    query_df['total_app_opens'] = pd.to_numeric(query_df['total_app_opens'],errors='coerce')
    query_df['total_app_opens_fmt']=query_df['total_app_opens'].apply(human_format)
    fig = px.bar(
                query_df.sort_values("total_app_opens", ascending=False),  # sort for cleaner horizontal bars
                x="total_app_opens",
                y="States",
                orientation="h",
                title=f"Underperforming States (Low App Opens < 100,000)",
                text="total_app_opens_fmt",  # show values on bars
                color="total_app_opens",  # add gradient coloring
            )
    st.plotly_chart(fig)
    bottom_df =query_df.nsmallest(5,'total_app_opens')
    col1,col2=st.columns(2)
    with col1:
        fig2=px.bar(
            bottom_df.sort_values("total_app_opens", ascending=True),
            x="total_app_opens",
            y="States",
            orientation="h",
            title="Bottom 5 States by App Opens",
            text="total_app_opens_fmt",
            color="total_app_opens",
        )
        st.plotly_chart(fig2)
    cursor.execute(f''' SELECT states,round(SUM(AppOpens)/SUM(RegisteredUsers),2) AS engagement_ratio
                        FROM map_user
                        GROUP BY states
                        having engagement_ratio < 28
                        ORDER BY engagement_ratio 
                        ''')
    conn.commit()
    query2=cursor.fetchall()
    query2_df=pd.DataFrame(query2,columns=['States','engagement_ratio'])
    query2_df['engagement_ratio'] = pd.to_numeric(query2_df['engagement_ratio'],errors='coerce')
    
    bottom_df2 =query2_df.nsmallest(5,'engagement_ratio')
    with col2:
        fig3=px.bar(
            bottom_df2.sort_values("engagement_ratio", ascending=True),
            x="engagement_ratio",
            y="States",
            orientation="h",
            title="Bottom 5 States by Engagement Ratio",
            text="engagement_ratio",
            color="engagement_ratio",
        )
        st.plotly_chart(fig3)






# ---------------------------------------------------------------------------------------------------------------------------#

# Streamlit page configuration
st.set_page_config(page_title="PhonePe Data Analysis", page_icon=":bar_chart:", layout="wide")
st.title("PhonePe Data Analysis")

# Sidebar for navigation


with st.sidebar:
    select = option_menu(
                menu_title="Menu",
                options=["Home", "Data Analysis", "Business"], # options
                icons=["house", "bar-chart", "briefcase"],  # icons for each option
                menu_icon="cast",  # icon for the menu
                default_index=0,
)

# Display content based on selection
if select == "Home":
    st.subheader("Welcome to the PhonePe Data Analysis App")
    st.write("Use the sidebar to navigate through different sections.")

elif select == "Data Analysis":
    st.subheader("Data Analysis Section")
    tab1,tab2,tab3=st.tabs(["Aggregate Analysis","Map Analysis","Top Analysis"])

    with tab1:

        method1=st.radio("Select the Method",('Insurance Analysis','Transaction Analysis','User Analysis'))

        if method1=='Insurance Analysis':
            
            col1,col2 = st.columns(2)

            with col1:
                year = st.selectbox("Select the Year",Aggre_insurance['Years'].unique())

            tac_y = Transaction_amount_count_Y(Aggre_insurance,year)

            col1,col2 = st.columns(2)
            with col1:
                quarter = st.selectbox("Select the Quarter",Aggre_insurance['Quarter'].unique())

            Transaction_amount_count_Y_Q(tac_y,quarter)

        elif method1=='Transaction Analysis':

            # this part of column is used for the year select of Transaction Analysis and a table is returned for the selected year 
            # later the returned table is used for the quarter selection and state selection

            col1,col2 = st.columns(2)
            with col1:
                year = st.selectbox("Select the Year",Aggre_transaction['Years'].unique())
            Aggre_trans_tac_y = Transaction_amount_count_Y(Aggre_transaction,year) 

            # this part of column is used for the state selection of Transaction Analysis type for the above selected year and a pie chart is returned for the selected state
            # here no table is returned because the pie chart is the final output for the state selection

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State",Aggre_trans_tac_y['States'].unique())
            Aggre_Transaction_Type(Aggre_trans_tac_y,states)   

            # this part of column is used for the quarter selection of Transaction Analysis and a table is returned for the selected quarter
            # later the returned table is used for the state selection and pie chart is returned for the selected state

            col1,col2 = st.columns(2)
            with col1:
                quarter = st.selectbox("Select the Quarter",Aggre_trans_tac_y['Quarter'].unique())

            Aggre_trans_tac_y_Q = Transaction_amount_count_Y_Q(Aggre_trans_tac_y,quarter) 

            # this part of column is used for the state selection of Transaction type Analysis for selected quarter above and a pie chart is returned for the selected state
            # here no table is returned because the pie chart is the final output for the state selection
            
            col1,col2 = st.columns(2)

            with col1:
                states = st.selectbox("Select the State_Quarter",Aggre_trans_tac_y_Q['States'].unique())
            Aggre_Transaction_Type(Aggre_trans_tac_y_Q,states)   

        elif method1=='User Analysis':
            col1,col2 = st.columns(2)
            with col1:
                year = st.selectbox("Select the Year",Aggre_user['Years'].unique())

            Aggre_user_Y=Aggre_user_brand_y(Aggre_user,year)  

            col1,col2 = st.columns(2)
            with col1:
                quarter = st.selectbox("Select the Quarter",Aggre_user_Y['Quarter'].unique())

            Aggre_user_Y_Q = Aggre_user_brand_Y_Q(Aggre_user_Y,quarter)

            col1,col2 = st.columns(2)
            with col1:
                state = st.selectbox("Select the Quarter_State",Aggre_user_Y_Q['States'].unique())

            Aggre_user_brand_y_q_state(Aggre_user_Y_Q,state)


# ---------------------------------------------------------------------------------------------------------------------------#

    with tab2:
        method2=st.radio("Select the Method",('Map Insurance','Map Transaction','Map User'))

        if method2=='Map Insurance':

            # year wise analysis for all states for Map Insurance table

            col1,col2 = st.columns(2)
            with col1:
                year = st.selectbox("Select the Insurance Year",Map_insurance['Years'].unique())
            map_insurance_amt_count = Transaction_amount_count_Y(Map_insurance,year)

            # District wise analysis for the selected year and state for Map Insurance table

            col1,col2 = st.columns(2)
            with col1:
                state = st.selectbox("Select the State_MapIns",map_insurance_amt_count['States'].unique())
            Map_insurance_district(map_insurance_amt_count,state)

            # quarter wise analysis for the selected year for Map Insurance table

            col1,col2 = st.columns(2)
            with col1:
                quarter = st.selectbox("Select the Insurance Quarter",map_insurance_amt_count['Quarter'].unique())
            Map_insurance_amt_count_Y_Q = Transaction_amount_count_Y_Q(map_insurance_amt_count,quarter)

            # state wise analysis for the selected year and quarter for Map Insurance table

            col1,col2 = st.columns(2)
            with col1:
                state = st.selectbox("Select the State_MapIns_Quarter",Map_insurance_amt_count_Y_Q['States'].unique())
            Map_insurance_district(Map_insurance_amt_count_Y_Q,state)

        elif method2=='Map Transaction':

            # year wise analysis for all states for Map Transaction table

            col1,col2 = st.columns(2)
            with col1:
                year = st.selectbox("Select the Transaction Year",Map_transaction['Years'].unique())
            map_transaction_amt_count_Y = Transaction_amount_count_Y(Map_transaction,year)

            # District wise analysis for the selected year and state for Map Transaction table

            col1,col2 = st.columns(2)
            with col1:
                state = st.selectbox("Select the State_MapTrans",map_transaction_amt_count_Y['States'].unique())
            Map_insurance_district(map_transaction_amt_count_Y,state)

            # quarter wise analysis for the selected year for Map Transaction table

            col1,col2 = st.columns(2)
            with col1:
                quarter = st.selectbox("Select the Transaction Quarter",map_transaction_amt_count_Y['Quarter'].unique())
            Map_transaction_amt_count_Y_Q = Transaction_amount_count_Y_Q(map_transaction_amt_count_Y,quarter)

            # District wise analysis for the selected year and quarter for Map Transaction table    

            col1,col2 = st.columns(2)
            with col1:
                state = st.selectbox("Select the State_MapTrans_Quarter",Map_transaction_amt_count_Y_Q['States'].unique())
            Map_insurance_district(Map_transaction_amt_count_Y_Q,state)

        elif method2=='Map User':

            col1,col2 = st.columns(2)
            with col1:
                year = st.selectbox("Select the User Year",Map_user['Years'].unique())
            map_user_y = Map_User_State_plot(Map_user,year)

            col1,col2 =st.columns(2)
            with col1:
                quarter = st.selectbox(f'Select the User Quarter for {year}',map_user_y['Quarter'].unique())
            Map_user_state = Map_User_State_plot_Y_Q(map_user_y,quarter)

            col1,col2=st.columns(2)
            with col1:
                state=st.selectbox(f'Select the User State for {year} year and {quarter} quarter',Map_user_state['States'].unique())
            Map_User_state_plot_Q(Map_user_state,state)



# ---------------------------------------------------------------------------------------------------------------------------#
    
    with tab3:
        method3=st.radio("Select the Method",('Top Insurance','Top Transaction','Top User'))
        if method3=='Top Insurance':
            col1,col2 = st.columns(2)
            with col1:
                year = st.selectbox("Select the Top Insurance Year",Top_insurance['Years'].unique())
            Top_insurance_amt_count_Y = Transaction_amount_count_Y(Top_insurance,year)

            # this part of column would show the transaction amount and count by quarter for the selected state and above selected year 
            col1,col2 = st.columns(2)
            with col1:
                state = st.selectbox("Select the Top Insurance State",Top_insurance_amt_count_Y['States'].unique())
            Top_insurance_amt_count_Y_Q(Top_insurance_amt_count_Y,state)

            col1,col2 = st.columns(2)
            with col1:
                quarter = st.selectbox("Select the Top Insurance Quarter",Top_insurance_amt_count_Y['Quarter'].unique())
            Top_insurance_amt_count_Y_Q = Transaction_amount_count_Y_Q(Top_insurance_amt_count_Y,quarter)

        elif method3=='Top Transaction':
            
            col1,col2 = st.columns(2)
            with col1:
                year = st.selectbox("Select the Top Transaction Year",Top_transaction['Years'].unique())
            Top_transaction_amt_count_Y = Transaction_amount_count_Y(Top_transaction,year)

            col1,col2 = st.columns(2)
            with col1:
                quarter = st.selectbox("Select the Top Transaction Quarter",Top_transaction_amt_count_Y['Quarter'].unique())
            Top_transaction_amt_count_Y_Q = Transaction_amount_count_Y_Q(Top_transaction_amt_count_Y,quarter)

        elif method3=='Top User':
            col1,col2 = st.columns(2)
            with col1:
                year = st.selectbox("Select the Top User Year",Top_user['Years'].unique())
            Top_User_Y =Top_User_analysis_Y(Top_user,year)

            col1,col2 = st.columns(2)
            with col1:
                state = st.selectbox("Select the Top User State",Top_User_Y['States'].unique())
            Top_user_state_plot_Y(Top_User_Y,year)

elif select == "Business":
    option = st.selectbox(
        "Business Analysis Options",
        ["Decoding Transaction Dynamics on PhonePe"
         ,"Device Dominance and User Engagement",
         "Insurance Penetration and Growth Potential",
         "Transaction Analysis for Market Expansion",
         "User Engagement and Growth Strategy"]
    )

    

    if option == "Decoding Transaction Dynamics on PhonePe":
        st.subheader("Decoding Transaction Dynamics on PhonePe")

        problem1 = st.selectbox("Select the Problem",
                                ["Total transactions by state", 
                                "Quarterly And Yearly Transaction Trend", 
                                "Transaction type contribution",
                                "Fastest growing state (YoY growth)", 
                                "States with declining transactions"])
        
        if problem1 == "Total transactions by state":


            cursor.execute("""select States,sum(Transaction_count) as Total_Transaction_count
                from aggregated_transaction
                group by States
                order by Total_Transaction_count desc""")
            conn.commit()
            query1 = cursor.fetchall()
            query1_df = pd.DataFrame(query1, columns=['States', 'Total_Transaction_count'])
            query1_df['Total_Transaction_count_fmt'] =query1_df['Total_Transaction_count'].apply(human_format)
            fig1 = px.bar(
            query1_df.sort_values("Total_Transaction_count", ascending=True),  # sort for cleaner horizontal bars
            x="Total_Transaction_count",
            y="States",
            orientation="h",
            title="Total Transaction Count in Each State",
            text="Total_Transaction_count_fmt",  # show values on bars
            color="Total_Transaction_count",  # add gradient coloring
            color_continuous_scale="Blues"   # color scheme
        )
            st.plotly_chart(fig1)

            state = st.selectbox("select the state",Aggre_transaction['States'].unique())
            district_wise_transaction_count(state)

        # query 2 Problem 1
        elif problem1 == "Quarterly And Yearly Transaction Trend":

            year=st.selectbox("select the year",Aggre_transaction['Years'].unique())
            yearly_transaction_count_analysis(year)

            quarter=st.selectbox("select the quarter",Aggre_transaction['Quarter'].unique())
            quarterly_transaction_count_analysis(year,quarter)

        # query 3 Problem 1
        elif problem1 == "Transaction type contribution":

            transaction_type_contribution()
            year=st.selectbox("select the year for transaction type contribution",Aggre_transaction['Years'].unique())
            transaction_type_contribution_Y(year)
            
        # query 4 Problem 1
        elif problem1 == "Fastest growing state (YoY growth)":
            # the growth percentage is slower as compared to the growth in transaction amount
            fastest_growing_state_yoy_growth()
            state=st.selectbox("select the state for fastest growing state YoY growth",Aggre_transaction['States'].unique())
            fastest_growing_state_yoy_growth_state(state)

        # query 5 Problem 1
        elif problem1 == "States with declining transactions":
            
            state=st.selectbox("select the state for declining transaction amount states yearwise",Aggre_transaction['States'].unique())
            declining_transaction_amount_states_yearwise(state)

            states=declining_transaction_amount_states()
            st.write("States with declining transaction amount over the years:")
            state2=st.selectbox("Select the state", states)
            declining_transaction_amount_states_yearwise(state2)

        
        


    elif option == "Device Dominance and User Engagement":
        st.subheader("Device Dominance and User Engagement")

        problem1 = st.selectbox("Select the Problem",
                                ["Registered users by brand", 
                                "Most engaged brand (highest %)", 
                                "Brand share by state",
                                "Top device in each quarter", 
                                "Underutilized devices"])
        
        if problem1 == "Registered users by brand":
            registered_users_by_brand()
            brand=st.selectbox("select the year for registered users by brand",Aggre_user['Brand'].unique())
            registered_users_by_brand_YOY(brand)

        elif problem1 == "Most engaged brand (highest %)":
            most_engaged_brand_highest_percentage()
            year=st.selectbox("select the year for most engaged brand highest percentage",Aggre_user['Years'].unique())
            most_engaged_brand_highest_percentage_yearly(year)
            state=st.selectbox("select the state for most engaged brand highest percentage",Aggre_user['States'].unique())
            most_engaged_brand_highest_percentage_state(year,state)
            
        elif problem1 == "Brand share by state":
            brand_share_by_state()

        elif problem1 == "Top device in each quarter":
            year=st.selectbox("select the year for top device in each quarter",Aggre_user['Years'].unique())
            top_device_in_each_quarter_year(year)
            quarter=st.selectbox("select the quarter for top device in given quarter",Aggre_user['Quarter'].unique())
            top_device_in_given_quarter(year,quarter)

        elif problem1 == "Underutilized devices":
            underutilized_devices()

    if option == "Insurance Penetration and Growth Potential":
        st.subheader("Insurance Penetration and Growth Potential")  
        problem1 = st.selectbox("Select the Problem",
                                ["Insurance penetration by state", 
                                "Yearly and quarterly trends", 
                                "States with highest penetration",
                                "Fastest growing state", 
                                "Untapped states (low insurance count)"])  
        if problem1 == "Insurance penetration by state":
            state_wise_insurance_penetration()
        elif problem1 == "Yearly and quarterly trends":
            state=st.selectbox("select the state for quarterly growth trend",Aggre_insurance['States'].unique())
            quarterly_growth_trend_state(state)
        elif problem1 == "States with highest penetration":
            states_with_highest_penetration()
        elif problem1 == "Fastest growing state":
            fastest_growing_state()
            state=st.selectbox("select the state for fastest growing state",Aggre_insurance['States'].unique())
            fastest_growing_state_selected(state)
        elif problem1 == "Untapped states (low insurance count)":
            untapped_states_low_insurance_count()

    if option == "Transaction Analysis for Market Expansion":
        st.subheader("Transaction Analysis for Market Expansion")
        problem1 = st.selectbox("Select the Problem",
                                ["State contribution share", 
                                "Districts with highest transaction count", 
                                "Yearly growth rate",
                                "Quarter with peak transactions", 
                                "Compare top vs bottom states"])
        if problem1 == "State contribution share":
            state_contribution_share()
        if problem1 == "Districts with highest transaction count":
            state=st.selectbox("select the state for districts with highest transaction count",Map_transaction['States'].unique())
            districts_with_highest_transaction_count(state)
            year=st.selectbox("select the year for districts with highest transaction count",Map_transaction['Years'].unique())
            districts_with_highest_transaction_count_year(year,state)
        if problem1 == "Yearly growth rate":
            yearly_growth_rate()
            state=st.selectbox("select the state for yearly growth rate",Aggre_transaction['States'].unique())
            yearly_growth_rate_selected(state)
        if problem1 == "Quarter with peak transactions":
            quarter_with_peak_transactions()
            state=st.selectbox("select the state for quarter with peak transactions",Aggre_transaction['States'].unique())
            quarter_with_peak_transactions_state(state)
        if problem1 == "Compare top vs bottom states":
            compare_top_vs_bottom_states()

    if option == "User Engagement and Growth Strategy":
        st.subheader("User Engagement and Growth Strategy")
        problem1 = st.selectbox("Select the Problem",
                                ["Total registered users per state", 
                                "App opens vs registered users", 
                                "Districts with highest engagement",
                                "Growth trend over years", 
                                "Underperforming states (low app opens)"])
        if problem1 == "Total registered users per state":
            total_registered_users_per_state()
            state=st.selectbox("select the state for total registered users",Map_user['States'].unique())
            total_registered_users_selected_state(state)

        if problem1 == "App opens vs registered users":
            app_opens_vs_registered_users()
            state=st.selectbox("select the state for app opens vs registered users",Map_user['States'].unique())
            engagement_ratio_yearly_state(state)
        
        if problem1 == "Districts with highest engagement":
            overall_highest_engagement_district()
            state=st.selectbox("select the state for districts with highest engagement",Map_user['States'].unique())
            districts_with_highest_engagement(state)
        if problem1 == "Growth trend over years":
            state=st.selectbox("select the state for growth trend over years",Map_user['States'].unique())
            growth_trend_over_years(state)
            forecast_trend_Regusers(state,forecast_years=3)
        if problem1 == "Underperforming states (low app opens)":
            underperforming_states_low_app_opens()