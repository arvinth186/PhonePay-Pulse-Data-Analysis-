# PhonePay-Pulse-Data-Analysis
This project is an end-to-end data engineering & analytics pipeline built on the PhonePe Pulse GitHub repository.

It extracts raw data from JSON files, transforms them into structured formats, loads them into a MySQL database, and enables business insights via SQL queries and Python visualizations.

The project is designed to analyze digital payment adoption trends in India across multiple dimensions:
<ol>
  
  <li>Transactions (type, count, amount)</li>
  <br>
  <li>Users (registrations, engagement, device brands)</li>
  <br>
  <li>Insurance adoption (counts, premiums)</li>
  <br>
  <li>Geography (state, district, pincode level trends)</li>
</ol>

<hr>

<h2>🔹<b>Tech Stack</b></h2>
<ol>
  <li>Python → Data extraction, transformation, and loading (ETL)</li>
  <br>
  <li>Pandas → Data preprocessing</li>
  <br>
  <li>JSON → Parsing PhonePe Pulse raw data</li>
  <br>
  <li>PyMySQL → Database connectivity with MySQL</li>
  <br>
  <li>MySQL → Data storage and SQL-based analysis</li>
  <br>
  <li>Plotly / Streamlit → Interactive dashboards & visualizations</li>
</ol>
<hr>
<h2>🔹Data Source</h2>

The dataset is obtained from: PhonePe Pulse GitHub Repository.
<br>
The data is structured in JSON format, organized by:

<ul>
  <li>Country → India</li>
  <br>
  <li>State → Individual state folders</li>
  <br>
  <li>Year → Subfolders</li>
  <br>
  <li>Quarter → JSON files</li>
</ul>

<hr>

<h2>🔹Database Schema</h2>

The project creates 9 MySQL tables, grouped into three categories:

<ol>
<li>Aggregated Tables</li>
<ul>
  
`aggregated_transaction` → Transactions by state, year, quarter, type

`aggregated_user` → Device brand-wise users and engagement %

`aggregated_insurance` → Insurance policies count & premiums
</ul>

<li>Map Tables</li>
<ul>
  
`map_transaction` → Transactions at state & district level

`map_user` → User registrations & app opens at state & district level

`map_insurance` → Insurance at state & district level
</ul>

<li>Top Tables</li>
<ul>
  
`top_transaction` → Top-performing states, districts, pincodes (transactions)

`top_user` → Top states/districts/pincodes by user registrations

`top_insurance` → Top states/districts/pincodes by insurance adoption
</ul>
</ol>

<hr>

<h2>🔹Workflow</h2>

Step 1: Data Extraction
<ul>
<li>Navigate the Pulse repository JSON files (os.listdir()).</li>

<li>Open each file and parse it using json.load().</li>

<li>Extract relevant fields (e.g., transactionData, usersByDevice).</li>
</ul>

Step 2: Data Transformation
<ul>
<li>Store extracted values into Python dictionaries.</li>

<li>Convert dictionaries into Pandas DataFrames.</li>

<li>Clean column names & convert data types.</li>
</ul>

Step 3: Data Loading
<ul>
<li>Connect to MySQL using pymysql.connect().</li>

<li>Create tables (CREATE TABLE IF NOT EXISTS).</li>

<li>Bulk insert DataFrame rows using executemany().</li>

<li>Commit inserts with conn.commit().</li>
</ul>

Step 4: Analysis
<ul>
<li>Run SQL queries for business insights</li>

<li>State-level transaction growth</li>

<li>Device dominance (Samsung vs Apple)</li>

<li>Insurance penetration by state</li>

<li>Top-performing districts/pincode</li>
</ul>
<hr>

<h2>SQL Query Analysis</h2>
<ol>
  <li><h3>Decoding Transaction Dynamics on PhonePe</h3></li>
  <p>
    PhonePe has noticed variations in transaction behavior across states, quarters, and transaction categories.
    
  Some regions show growth.
  Others show stagnation or decline.
  
  Leadership wants to know where, when, and why these differences happen.
    
  👉 The goal is to decode transaction dynamics → identify patterns, trends, and anomalies in user transactions.
  </p>
  <h4>Business Scenarios Addressed:</h4>
  <ol>
    <li>Total transactions by state</li>
    <li>Quarterly transaction trend</li>
    <li>Transaction type contribution</li>
    <li>Fastest growing state (YoY growth)</li>
    <li>States with declining transactions</li>
  </ol>
  <li><h3>Device Dominance and User Engagement</h3></li>
  <p>
    PhonePe wants to understand how user engagement varies across device brands (Samsung, Xiaomi, Apple, etc.).

They see differences between registered users vs. actual app usage (App Opens %).

Some brands have high registrations but low engagement (underutilized).

Leadership wants to know which devices are most dominant and where there is untapped potential.

👉 The goal is to analyze device dominance and engagement patterns to improve app performance and marketing strategy.
  </p>
  <h4>Business Scenarios Addressed:</h4>
  <ol>
    <li>Registered users by brand</li>
    <li>Most engaged brand (highest %)</li>
    <li>Brand share by state</li>
    <li>Top device in each quarter</li>
    <li>Underutilized devices (low engagement %)</li>
  </ol>
  <li><h3>Insurance Penetration and Growth Potential</h3></li>
  <p>
    PhonePe has expanded into insurance services.

They want to know how well insurance is being adopted across states, quarters, and years.

The company is looking for growth patterns and untapped regions where insurance adoption is low.

Insights are needed to prioritize marketing, partnerships, and product strategy.

👉 The core problem: Which states show strong insurance adoption, which lag behind, and what is the overall growth potential?
  </p>
  <h4>Business Scenarios Addressed:</h4>
  <ol>
    <li>Total insurance by state</li>
    <li>Quarterly growth trend</li>
    <li>States with highest penetration (avg premium)</li>
    <li>Fastest growing states</li>
    <li>Untapped states (low insurance count)</li>
  </ol>
  <li><h3>Transaction Analysis for Market Expansion</h3></li>
  <p>
    1) Problem Statement

PhonePe operates in a highly competitive digital payments market.

To expand into new markets, the leadership needs to understand where transaction activity is high, where it’s growing, and where it’s lagging.

The aim is to identify trends, opportunities, and expansion areas at the state and district level.

👉 The core problem: Which states/districts should PhonePe target for future growth, based on transaction volume, value, and trends?
  </p>
  <h4>Business Scenarios Addressed:</h4>
  <ol>
    <li>State contribution share</li>
    <li>Districts with highest transaction count</li>
    <li>Yearly growth rate</li>
    <li>Quarter with peak transactions</li>
    <li>Compare top vs bottom states</li>
  </ol>
  <li><h3>User Engagement and Growth Strategy</h3></li>
  <p>
    PhonePe wants to strengthen its market position by analyzing user engagement.

Engagement is measured using registered users and app opens.

There are large variations across states and districts.

The business wants to know where users are most engaged, where growth is strong, and where engagement is weak.

👉 The main problem: Which regions have high engagement and growth potential, and which need attention to improve adoption and usage?
  </p>
  <h4>Business Scenarios Addressed:</h4>
  <ol>
    <li>Total registered users per state</li>
    <li>App opens vs registered users (engagement ratio)</li>
    <li>Districts with highest engagement</li>
    <li>Growth trend over years</li>
    <li>Underperforming states (low app opens)</li>
  </ol>
</ol>
<hr>
<h2>🔹How to Run</h2>
<ol>
  <li><h3>Clone the PhonePe Pulse Repo</h3></li>
  
  ```bash
  git clone https://github.com/PhonePe/pulse
```
<li>Install dependencies</li>

```bash
pip install pymysql pandas plotly

```
<li>Set up MySQL</li>

```sql
CREATE DATABASE phonepay;
```
<li>Run the Notebook</li>
<ul>
  <li>Open Phonepay.ipynb in Jupyter/VS Code</li>
  <li>Update the host, user, password in MySQL connection</li>
  <li>Execute cells sequentially</li>
</ul>
</ol>
<hr>
<h2>🔹Future Enhancements</h2>
<ul>
  <li>Automate ETL pipeline using Airflow or Prefect</li>
  <li>Deploy dashboards using Streamlit / Power BI</li>
  <li>Add indexes & primary keys in MySQL for better performance</li>
  <li>Integrate real-time data updates if PhonePe Pulse offers API</li>
</ul>
<h2>🔹Author</h2>
📌 Developed by: Arvinth AthiKesav<br>
📌 Purpose: Data Engineering & Analytics Case Study using PhonePe Pulse Dataset



