# RetailIQ: Global Retail Sales & Profitability Intelligence

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg?logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Power BI](https://img.shields.io/badge/Power%20BI-Desktop-F2C811.svg?logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

RetailIQ is an end-to-end retail business intelligence project that transforms raw multi-national transactional data into executive-level commercial insights. Spanning 51,290 transactions across 147 countries (2011–2014), the project implements a complete analytics lifecycle: Python-based data profiling, automated data hygiene and feature engineering, relational schema design and complex analytical querying in MySQL, and an interactive executive dashboard in Microsoft Power BI.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Problem Statement](#problem-statement)
- [Objectives](#objectives)
- [Dataset Details](#dataset-details)
- [Tools & Technologies](#tools--technologies)
- [Data Preparation & Cleaning](#data-preparation--cleaning)
- [Analysis Performed](#analysis-performed)
- [Key Performance Indicators (KPIs)](#key-performance-indicators-kpis)
- [Power BI Dashboard & Visuals](#power-bi-dashboard--visuals)
- [Key Business Insights](#key-business-insights)
- [Project Structure](#project-structure)
- [How to Run and View the Project](#how-to-run-and-view-the-project)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Author](#author)

---

## Project Overview

In multi-regional retail enterprises, aggregate revenue growth often masks severe operational inefficiencies, regional margin erosions, and deeply unprofitable product lines. RetailIQ evaluates the performance of the Global Superstore commercial operation across four consecutive operating years (2011–2014).

By bridging **Python (ETL & feature engineering)**, **MySQL (relational data modeling & SQL analytics)**, and **Power BI (DAX modeling & executive visualization)**, RetailIQ provides senior leadership with a consolidated single source of truth for margin preservation, discounting policy reform, and logistics turnaround monitoring.

---

## Problem Statement

While top-line gross merchandise value reached **\$12.64M**, leadership lacked visibility into underlying margin leakage across 7 global markets and 17 sub-categories. Specifically:
1. **Unprofitable Transactions**: Almost 25% of all order line items generated negative profit, indicating unchecked discounting and misaligned shipping cost absorption.
2. **Category Margin Disparity**: High-revenue categories such as Furniture suffered from severe margin compression compared to Technology and Office Supplies.
3. **Logistics Latency**: Fulfillment times varied significantly across shipping modes, directly impacting fulfillment expenses and customer experience.
4. **Account Profit Volatility**: Certain high-spending VIP customers incurred substantial cumulative losses for the business.

---

## Objectives

- **Audit & Cleanse Data**: Profile and clean 51,290 raw transaction records with zero tolerance for missing timestamps or whitespace anomalies.
- **Engineer Business Dimensions**: Formulate derived analytical dimensions (order year, month, quarter, transit durations, and transaction-level profit margins).
- **Relational Warehousing**: Ingest clean records into MySQL using SQLAlchemy and execute 10 business-focused SQL queries.
- **Interactive Executive Dashboard**: Build a Power BI dashboard equipped with interactive slicing (Year, Market, Category, Segment) and DAX measures.
- **Empirical Strategy Formulation**: Identify exact loss-making products, underperforming markets, and discounting thresholds.

---

## Dataset Details

The project utilizes the **Global Superstore** transactional dataset.

| Attribute | Value |
|---|---|
| **Raw Records** | 51,290 rows |
| **Raw Columns** | 23 attributes |
| **Cleaned Columns** | 28 attributes (5 engineered features added) |
| **Time Period** | January 1, 2011 – December 31, 2014 (4 Full Years) |
| **Geographic Coverage** | 147 Countries, 7 Markets (APAC, EU, US, LATAM, EMEA, Africa, Canada), 13 Regions |
| **Order Volume** | 25,035 Unique Orders |
| **Customer Base** | 1,740 Unique Customers across 3 Segments (Consumer, Corporate, Home Office) |
| **Catalog Breadth** | 3 Categories, 17 Sub-Categories, 3,788 Distinct Products |

### Primary Attributes:
- **Order Identifiers & Dates**: `Order ID`, `Order Date`, `Ship Date`, `Ship Mode`, `Order Priority`
- **Customer Profiles**: `Customer ID`, `Customer Name`, `Segment`, `City`, `State`, `Country`, `Market`, `Region`
- **Product Hierarchy**: `Product ID`, `Category`, `Sub-Category`, `Product Name`
- **Financial Metrics**: `Sales`, `Quantity`, `Discount`, `Profit`, `Shipping Cost`

---

## Tools & Technologies

- **Python 3**:
  - `pandas`: Data profiling, date parsing, string sanitization, and feature engineering.
  - `SQLAlchemy`: Relational engine interface for automated database schema generation.
  - `PyMySQL`: High-performance MySQL database connector.
  - `python-dotenv`: Environment variable management to prevent credential leakage.
- **MySQL 8.x**: Relational database storage, data indexing, and execution of business queries.
- **Microsoft Power BI Desktop**: Data model development, VertiPaq internal caching, DAX measures, and interactive executive reporting.
- **Git & GitHub**: Version control, security hardening, and portfolio publication.

---

## Data Preparation & Cleaning

Implemented in `python/01_data_profiling.py` and `python/02_data_cleaning.py`:

1. **Structural Profiling**:
   - Analyzed 51,290 records to confirm zero duplicated order-item rows.
   - Identified missing value distribution (`Postal Code` contained nulls in international rows, retained without affecting core financial logic).
2. **Temporal Parsing**:
   - Converted `Order Date` and `Ship Date` to standardized `datetime64[ns]` with `dayfirst=True` to eliminate ambiguous date ordering.
3. **Text Sanitization**:
   - Dynamically selected all object/string columns (`Category`, `Sub-Category`, `Customer Name`, `Market`, etc.) and stripped leading/trailing whitespace.
4. **Feature Engineering**:
   - `Order Year`: Calendar year (`dt.year`) for annual performance benchmarking.
   - `Order Month`: Full month name (`dt.month_name()`) for seasonality analysis.
   - `Order Quarter`: Fiscal quarter (`dt.quarter`) for quarterly business reviews.
   - `Shipping Days`: Fulfillment duration calculated as `(Ship Date - Order Date).dt.days`.
   - `Profit Margin (%)`: Transaction-level efficiency calculated as `(Profit / Sales) * 100`.
5. **Output**: Exported verified clean dataset to `data/cleaned_superstore.csv`.

---

## Analysis Performed

The SQL analytics layer (`sql/02_business_queries.sql`) and data profiling scripts executed the following 10 structured analytical investigations:

1. **Overall Commercial Performance**: Aggregated cumulative gross revenue, total profits, units sold, and unique transaction counts.
2. **Category Performance Ranking**: Comparative revenue, profit, and margin breakdown across Technology, Furniture, and Office Supplies.
3. **Top 10 Products by Revenue**: Identified primary revenue generators and their corresponding net profit contribution.
4. **Top 10 Customers by Lifetime Value**: Ranked top enterprise and retail accounts by gross spend and evaluated account-level profitability.
5. **Market Dynamics**: Evaluated sales volume and operating margins across all 7 global sales regions.
6. **Chronological Sales Trends**: Mapped monthly sales progression chronologically from 2011 through 2014 to identify recurring demand surges.
7. **Regional Profitability Variance**: Pinpointed high-margin territories versus margin-diluted zones across 13 geographic regions.
8. **Category Discount Analysis**: Computed average discount rates across merchandise categories to assess correlation with margin depression.
9. **Logistics & Turnaround by Ship Mode**: Calculated mean shipping durations across fulfillment classes (`Same Day`, `First Class`, `Second Class`, `Standard Class`).
10. **Top 10 Loss-Making Products**: Isolated worst-performing SKUs generating substantial negative cumulative profit.

---

## Key Performance Indicators (KPIs)

Empirical metrics calculated from the 51,290 transactions:

| Metric | Empirical Value | Description |
|---|---|---|
| **Total Revenue** | **\$12,642,501.91** | Cumulative gross merchandise sales (2011–2014) |
| **Total Profit** | **\$1,467,457.29** | Net cumulative operating profit |
| **Total Units Sold** | **178,312** | Total product units fulfilled |
| **Total Unique Orders** | **25,035** | Distinct order transactions |
| **Total Line Items** | **51,290** | Total individual order items processed |
| **Overall Profit Margin** | **11.61%** | Aggregate enterprise net profit margin |
| **Average Shipping Duration** | **3.97 Days** | Enterprise mean transit time from order to shipment |
| **Average Discount** | **14.29%** | Mean discount granted per line item |
| **Unprofitable Transactions** | **12,544 rows (24.46%)** | Line items resulting in negative net profit |
| **Break-Even Transactions** | **668 rows (1.30%)** | Line items resulting in exactly \$0.00 net profit |

---

## Power BI Dashboard & Visuals

The Power BI report file (`powerbi/RetailIQ_Dashboard.pbix`) consists of a custom-designed **Executive Overview** page (1280 × 720 canvas) designed for senior retail leadership:

### 1. KPI Cards (Top Banner)
- **Total Sales**: Formatted currency card tracking gross revenue.
- **Total Profit**: Formatted currency card displaying net profit.
- **Total Orders**: Card displaying distinct order transactions.
- **Total Quantity**: Card tracking cumulative merchandise units sold.
- **Profit Margin %**: Percentage card displaying aggregate margin health.
- **Avg Shipping Days**: Metric card displaying enterprise fulfillment turnaround.

### 2. Core Visualizations
- **Monthly Sales Trend (Line Chart)**: Continuous time-series plotting `Total Sales` across `Order Year` and `Order Month`, capturing annual end-of-year peaks.
- **Sales by Category (Treemap)**: Hierarchical treemap grouped by `Category` with `Sub-Category` details and sized by `Total Sales`.
- **Profit by Market (Clustered Bar Chart)**: Horizontal distribution ranking net profit across all 7 markets (`APAC`, `EU`, `US`, `LATAM`, `Africa`, `EMEA`, `Canada`).
- **Top 10 Customers by Revenue (Clustered Bar Chart)**: Account ranking displaying gross spend per client.
- **Top 10 Products (Clustered Bar Chart)**: Product-level ranking highlighting highest grossing hardware and furniture items.
- **Average Shipping Days by Ship Mode (Clustered Column Chart)**: Turnaround comparison across fulfillment classes.

### 3. Interactive Slicers & Controls
- **Order Year Slicer**: Toggle dynamic filtering across 2011, 2012, 2013, and 2014.
- **Market Slicer**: Geographic filter across 7 international markets.
- **Category Slicer**: Filter by `Technology`, `Furniture`, and `Office Supplies`.
- **Segment Slicer**: Filter by customer profile (`Consumer`, `Corporate`, `Home Office`).
- **Action Button**: Interactive canvas reset / bookmark navigation control.

---

## Key Business Insights

### 1. Technology Leads in Both Scale and Profitability
- **Technology** generated **\$4,744,557** in sales (37.5% of total revenue) and **\$663,779** in profit, yielding an above-average **13.99% profit margin**.
- Leading sub-categories include **Phones** (\$1.71M sales, \$216.7K profit) and **Copiers** (\$1.51M sales, \$258.6K profit, **17.13% margin**).
- The single most profitable product catalog line was the *Canon imageCLASS 2200 Advanced Copier*, delivering **\$25,200** in profit on **\$61,600** in sales (a 40.9% margin).

### 2. Furniture Margin Compression & Table Drain
- **Furniture** achieved **\$4,110,874** in sales but yielded only **\$285,205** in profit—a depressed margin of **6.94%**.
- The primary drag is the **Tables** sub-category: across 3,083 units sold, Tables generated **\$757,042** in sales but incurred an aggregate net loss of **-\$64,083.39** (**-8.46% profit margin**).
- Furniture suffered from the highest category average discount (**16.81%** vs. 13.53% for Technology).

### 3. Severe Loss-Making SKUs Require Immediate Rationalization
- Several high-cost hardware products generated massive bottom-line losses:
  - *Cubify CubeX 3D Printer Double Head Print*: Generated \$11,100 in sales but lost **-\$8,879.97**.
  - *Lexmark MX611dhe Monochrome Laser Printer*: Generated \$16,830 in sales but lost **-\$4,589.97**.
  - *Cubify CubeX 3D Printer Triple Head Print*: Generated \$8,000 in sales but lost **-\$3,839.99**.
- These losses stem from deep discounting coupled with high proportional shipping fees.

### 4. Geographic Profit Disparities
- **APAC** is the largest and most lucrative market (**\$3.59M sales**, **\$436.0K profit**, 12.16% margin), followed closely by the **EU** (**\$2.94M sales**, **\$372.8K profit**, 12.69% margin).
- **Southeast Asia** produced **\$884,423** in sales but yielded only **\$17,852** in net profit—a razor-thin margin of **2.02%**.
- **EMEA** also underperformed with a **5.45% margin** (\$43.9K profit on \$806.2K sales).
- Conversely, **Canada** demonstrated the highest operational margin at **26.62%** (\$17.8K profit on \$66.9K sales).

### 5. High Unprofitable Order Line Ratio (24.46%)
- **12,544 out of 51,290 lines** (24.46%) produced negative profit.
- One in every four items sold resulted in net margin destruction. Enforcing automated discount caps at the point of sale is the single highest-leverage operational recommendation.

### 6. High-Spend Customer Profit Inversion
- While top client *Tom Ashbrook* contributed **\$35,668** in sales and **\$6,275** in profit, client *Sean Miller* ranked #4 in total revenue (**\$31,125**) but resulted in a cumulative loss of **-\$1,083.67** due to discounted orders.

### 7. Fulfillment Performance
- Transit times matched service levels consistently:
  - `Same Day`: **0.04 days** (~1 hour processing) | 1,347 orders
  - `First Class`: **2.18 days** | 3,821 orders
  - `Second Class`: **3.23 days** | 5,119 orders
  - `Standard Class`: **5.00 days** | 15,154 orders (60.5% of all orders)

### 8. Consistent 4-Year Compound Growth
- Annual sales scaled steadily:
  - **2011**: \$2,259,451 sales | \$248,941 profit (4,440 orders)
  - **2012**: \$2,677,439 sales | \$307,415 profit (5,343 orders)
  - **2013**: \$3,405,746 sales | \$406,935 profit (6,721 orders)
  - **2014**: \$4,299,866 sales | \$504,166 profit (8,531 orders)
- Revenue grew **90.3%** and net profit doubled (**+102.5%**) over the four-year period.

---

## Project Structure

```plaintext
retailIQ/
│
├── data/
│   ├── README.md                      # Instructions for acquiring & placing dataset
│   ├── Global_Superstore22.csv        # Raw dataset (51,290 rows) [Excluded via .gitignore]
│   └── cleaned_superstore.csv         # Cleaned & engineered dataset [Excluded via .gitignore]
│
├── powerbi/
│   └── RetailIQ_Dashboard.pbix        # Interactive Power BI executive dashboard
│
├── python/
│   ├── 01_data_profiling.py           # Dataset inspection, shape, nulls, duplicates
│   ├── 02_data_cleaning.py            # Date conversion, string sanitization, feature engineering
│   ├── 03_feature_engineering.py      # Feature engineering architecture documentation
│   ├── 04_export_mysql.py             # Database export workflow documentation
│   └── 05_load_mysql.py               # Secure SQLAlchemy ETL pipeline to MySQL
│
├── sql/
│   ├── 01_create_database.sql         # Database initialization script
│   └── 02_business_queries.sql        # 10 core business intelligence SQL queries
│
├── reports/
│   └── .gitkeep                       # Directory for exported analytical summaries
│
├── screenshots/
│   └── .gitkeep                       # Directory for dashboard visuals & report previews
│
├── .env.example                       # Environment variable template for DB credentials
├── .gitignore                         # Git exclusion rules (secrets, venv, cache, datasets)
├── CONTEXT.md                         # Technical specification & context for future sessions
├── README.md                          # Project documentation and portfolio presentation
└── requirements.txt                   # Python library dependencies
```

---

## How to Run and View the Project

### Prerequisites
- Python 3.10+
- MySQL Server 8.0+
- Microsoft Power BI Desktop
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/retailIQ.git
cd retailIQ
```

### 2. Environment Setup
Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

Install required dependencies:
```bash
pip install -r requirements.txt
```

### 3. Configure Database Credentials
Copy `.env.example` to `.env` and update your MySQL connection details:
```bash
cp .env.example .env
```
Edit `.env`:
```env
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=retailiq
```

### 4. Execute Data Profiling & Cleaning
Run profiling:
```bash
cd python
python 01_data_profiling.py
```
Run cleaning and feature engineering (generates `data/cleaned_superstore.csv`):
```bash
python 02_data_cleaning.py
```

### 5. Initialize Database & Ingest Data
1. In MySQL Workbench or MySQL CLI, run:
   ```sql
   source ../sql/01_create_database.sql;
   ```
2. Ingest the dataset into MySQL:
   ```bash
   python 05_load_mysql.py
   ```
3. Run the analytical business queries:
   ```sql
   source ../sql/02_business_queries.sql;
   ```

### 6. Explore Power BI Dashboard
1. Open Microsoft Power BI Desktop.
2. Open `powerbi/RetailIQ_Dashboard.pbix`.
3. The dashboard is fully populated with cached model data. Use the slicers on the left canvas to explore trends by Year, Market, Category, and Segment.

---

## Limitations

1. **Static Batch Extract**: The pipeline processes a static historical CSV export rather than an incremental real-time streaming pipeline (e.g. Apache Kafka or Airflow).
2. **Cost-of-Goods-Sold (COGS) Granularity**: Product unit acquisition costs are inferred from the relationship between `Sales` and `Profit` without explicit itemized manufacturing cost breakdowns.
3. **Single-Page Executive Scope**: The current Power BI report concentrates on an all-in-one executive summary. Granular customer cohort and logistics drill-downs are slated for secondary pages.

---

## Future Improvements

- [ ] **Automated Data Quality Testing**: Integrate `Great Expectations` or `pytest` suites into the ETL pipeline to enforce schema contracts.
- [ ] **Customer Lifetime Value (CLV) & Churn Scoring**: Develop predictive machine learning models in Python to predict repeat purchase probability.
- [ ] **Multi-Page Power BI Expansion**: Add dedicated report pages for *Logistics & Fulfillment Optimization* and *Customer Segmentation Matrix*.
- [ ] **Automated Orchestration**: Package the Python-to-MySQL ETL workflow in Apache Airflow or GitHub Actions.

---

## Author

**Nakshi Goda**  
- **Role**: Data Analyst / Business Intelligence Developer  
- **Focus**: SQL Analytics, Python ETL Pipelines, Power BI Modeling & Visualization  
- **GitHub**: [@nakshigoda](https://github.com/) *(or your GitHub profile URL)*  
- **LinkedIn**: [Connect on LinkedIn](https://www.linkedin.com/)
