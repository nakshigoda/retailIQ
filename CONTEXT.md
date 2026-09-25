# RetailIQ: Technical Context & Development Guide

This document serves as the complete technical source of truth for the **RetailIQ** project. It is structured for developers, data analysts, and AI coding assistants collaborating on future iterations, maintenance, or feature extensions.

---

## 1. Project Purpose & Scope

RetailIQ is an end-to-end commercial analytics system designed to evaluate multi-market sales performance, identify profit margin erosion, audit shipping turnaround times, and detect loss-making merchandise.

### Business Objective
A multinational retailer operating across 147 countries requires empirical visibility into its global sales data. While aggregate revenue exceeds \$12.6M, approximately 24.5% of order lines operate at a net loss. RetailIQ was constructed to:
1. Provide a single source of truth for commercial transactions (2011–2014).
2. Cleanse and enrich raw transactional data with calendar, shipping, and margin features.
3. Centralize data into a relational database (MySQL) for business query execution.
4. Deliver an executive-ready Power BI dashboard with interactive slicers and measures.

---

## 2. Dataset Specification & Data Dictionary

### File References
- **Raw File**: `data/Global_Superstore22.csv` (11,989,093 bytes, 51,290 rows × 23 columns)
- **Processed File**: `data/cleaned_superstore.csv` (13,741,816 bytes, 51,290 rows × 28 columns)
- **Encoding**: `latin1` (ISO-8859-1) for raw CSV; UTF-8 for processed output.

### Column-Level Data Dictionary

| # | Column Name | Raw / Clean | Data Type | Description & Example Values |
|---|---|---|---|---|
| 1 | `Row ID` | Both | `int64` | Unique surrogate key for each transaction row (e.g., `1`, `32298`) |
| 2 | `Order ID` | Both | `object` / `VARCHAR(50)` | Business transaction identifier (e.g., `CA-2012-124891`, `IN-2013-77878`) |
| 3 | `Order Date` | Both | `datetime64[ns]` | Date customer placed order (`2011-01-01` to `2014-12-31`) |
| 4 | `Ship Date` | Both | `datetime64[ns]` | Fulfillment / shipment dispatch date |
| 5 | `Ship Mode` | Both | `object` / `VARCHAR(30)` | Dispatch service class (`First Class`, `Same Day`, `Second Class`, `Standard Class`) |
| 6 | `Customer ID` | Both | `object` / `VARCHAR(30)` | Customer account identifier (e.g., `TA-21385`, `GT-14710`) |
| 7 | `Customer Name` | Both | `object` / `VARCHAR(100)` | Full name of the purchasing customer (e.g., `Tom Ashbrook`) |
| 8 | `Segment` | Both | `object` / `VARCHAR(30)` | Customer classification (`Consumer`, `Corporate`, `Home Office`) |
| 9 | `City` | Both | `object` / `VARCHAR(100)` | Destination municipality |
| 10 | `State` | Both | `object` / `VARCHAR(100)` | Destination state / administrative province |
| 11 | `Country` | Both | `object` / `VARCHAR(100)` | Destination country (147 distinct countries) |
| 12 | `Market` | Both | `object` / `VARCHAR(20)` | Commercial macro-market (`APAC`, `EU`, `US`, `LATAM`, `EMEA`, `Africa`, `Canada`) |
| 13 | `Region` | Both | `object` / `VARCHAR(30)` | Geographic sales region (13 regions: `Central`, `North`, `North Asia`, `South`, etc.) |
| 14 | `Product ID` | Both | `object` / `VARCHAR(50)` | Product SKU identifier (e.g., `OFF-ST-10001968`) |
| 15 | `Category` | Both | `object` / `VARCHAR(50)` | High-level merchandise category (`Technology`, `Furniture`, `Office Supplies`) |
| 16 | `Sub-Category` | Both | `object` / `VARCHAR(50)` | Merchandise sub-category (17 sub-categories: `Phones`, `Copiers`, `Tables`, etc.) |
| 17 | `Product Name` | Both | `object` / `VARCHAR(255)` | Full catalog item description (3,788 distinct products) |
| 18 | `Sales` | Both | `float64` | Transaction gross merchandise revenue |
| 19 | `Quantity` | Both | `int64` | Unit count of product purchased |
| 20 | `Discount` | Both | `float64` | Decimal promotional discount rate applied (0.00 to 0.85) |
| 21 | `Profit` | Both | `float64` | Net financial profit (can be negative for loss-making sales) |
| 22 | `Shipping Cost` | Both | `float64` | Outbound fulfillment carrier cost |
| 23 | `Order Priority` | Both | `object` / `VARCHAR(20)` | Delivery urgency level (`Critical`, `High`, `Medium`, `Low`) |
| 24 | `Order Year` | Clean Only | `int64` | Calendar year extracted from `Order Date` (`2011`, `2012`, `2013`, `2014`) |
| 25 | `Order Month` | Clean Only | `object` | Full calendar month name (`January` – `December`) |
| 26 | `Order Quarter` | Clean Only | `int64` | Financial quarter (`1`, `2`, `3`, `4`) |
| 27 | `Shipping Days` | Clean Only | `int64` | Transit time: `(Ship Date - Order Date)` in integer days |
| 28 | `Profit Margin (%)` | Clean Only | `float64` | Line-item margin: `(Profit / Sales) * 100` |

---

## 3. Data Preparation & Transformation Pipeline

### Phase 1: Data Profiling (`python/01_data_profiling.py`)
- Analyzed dataset dimensions: 51,290 rows × 23 columns.
- Validated row-level uniqueness: `df.duplicated().sum() == 0`.
- Audited missing values: `df.isnull().sum()`.
  - Only `Postal Code` in standard Superstore data has missing entries (for non-US countries). The project uses columns that contain 0 missing values across all 51,290 rows.
- Evaluated category cardinalities:
  - 147 Countries, 7 Markets, 3 Categories, 17 Sub-Categories, 4 Ship Modes.

### Phase 2: Data Cleaning & Feature Engineering (`python/02_data_cleaning.py`)
- **Date Handling**:
  - `pd.to_datetime(df["Order Date"], dayfirst=True)`
  - `pd.to_datetime(df["Ship Date"], dayfirst=True)`
- **String Sanitization**:
  - Dynamic discovery of `object` and `string` dtypes followed by `.str.strip()` to remove leading and trailing whitespace.
- **Engineered Dimensions**:
  ```python
  df["Order Year"] = df["Order Date"].dt.year
  df["Order Month"] = df["Order Date"].dt.month_name()
  df["Order Quarter"] = df["Order Date"].dt.quarter
  df["Shipping Days"] = (df["Ship Date"] - df["Order Date"]).dt.days
  df["Profit Margin (%)"] = (df["Profit"] / df["Sales"]) * 100
  ```
- **Serialization**: Saved output directly to `data/cleaned_superstore.csv`.

### Phase 3: Relational Ingestion (`python/05_load_mysql.py`)
- Configured with SQLAlchemy engine: `mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}`.
- Refactored to utilize `os.getenv` via `python-dotenv` to eliminate committed credentials.
- Ingests `cleaned_superstore.csv` into table `sales` with `if_exists="replace"` and `index=False`.

---

## 4. SQL Analytics Layer & Business Questions Answered

Script: `sql/02_business_queries.sql`

| Query # | Target Focus | Analytical Purpose & SQL Logic | Key Metric / Result |
|---|---|---|---|
| **Q1** | **Overall Business Performance** | Aggregates `ROUND(SUM(Sales),2)`, `ROUND(SUM(Profit),2)`, `SUM(Quantity)`, and `COUNT(DISTINCT \`Order ID\`)` from `sales`. | Total Sales: \$12.64M, Total Profit: \$1.47M, Items: 178,312, Orders: 25,035. |
| **Q2** | **Category Performance** | Groups by `Category`, aggregates Sales and Profit, ordered by `Total_Sales DESC`. | Technology: \$4.74M Sales / \$663.8K Profit; Furniture: \$4.11M / \$285.2K; Office Supplies: \$3.79M / \$518.5K. |
| **Q3** | **Top 10 Products by Revenue** | Groups by `Product Name`, aggregates Sales & Profit, ordered by `Revenue DESC LIMIT 10`. | Led by Apple, Cisco, and Motorola smart phones; Canon copier generates highest profit (\$25.2K). |
| **Q4** | **Top 10 Customers by Spending** | Groups by `Customer Name`, aggregates Sales, ordered by `Total_Spent DESC LIMIT 10`. | Tom Ashbrook (\$35.7K), Greg Tran (\$34.5K), Tamara Chand (\$34.2K). Sean Miller (\$31.1K) incurred -\$1,083 loss. |
| **Q5** | **Market Performance** | Groups by `Market`, aggregates Sales & Profit, ordered by `Revenue DESC`. | APAC (\$3.59M) and EU (\$2.94M) are primary revenue/profit engines. |
| **Q6** | **Monthly Sales Trend** | Groups by `Order Year`, `Order Month`, ordered chronologically using MySQL `FIELD()`. | Q4 surge observed annually; November and December capture peak enterprise purchasing. |
| **Q7** | **Regional Profitability** | Groups by `Region`, aggregates Profit, ordered by `Total_Profit DESC`. | Central (\$311.4K) and North (\$194.6K) top profits; Southeast Asia ranks lowest in profit margin (2.02%). |
| **Q8** | **Category Discount Rates** | Groups by `Category`, calculates `ROUND(AVG(Discount)*100, 2)`. | Furniture has highest discount (16.81%), directly suppressing operating margins. |
| **Q9** | **Turnaround by Ship Mode** | Groups by `Ship Mode`, computes `ROUND(AVG(\`Shipping Days\`), 2)`. | Same Day: 0.04 days; First Class: 2.18 days; Second Class: 3.23 days; Standard Class: 5.00 days. |
| **Q10** | **Top 10 Loss-Making Products** | Groups by `Product Name`, aggregates Profit, ordered by `Total_Profit ASC LIMIT 10`. | Cubify 3D printers (-\$8.9K and -\$3.8K), Lexmark printers (-\$4.6K), Bevis tables (-\$3.6K). |

---

## 5. Enterprise KPIs (Empirical Totals)

- **Total Sales**: \$12,642,501.91
- **Total Profit**: \$1,467,457.29
- **Total Items Fulfilled**: 178,312 units
- **Total Orders**: 25,035 unique orders
- **Total Records (Order Lines)**: 51,290 lines
- **Enterprise Profit Margin**: 11.61%
- **Average Transit Time**: 3.97 days
- **Average Order Discount**: 14.29%
- **Negative Profit Lines**: 12,544 rows (24.46% of all transactions)
- **Zero Profit Lines**: 668 rows (1.30% of all transactions)

---

## 6. Power BI Dashboard Architecture

File: `powerbi/RetailIQ_Dashboard.pbix`

### Canvas & Theme
- **Report Page**: `Executive Overview` (Single-page canvas: 1280 × 720 px).
- **Embedded Cache**: VertiPaq internal data model (3.3 MB) contains loaded `sales` table.
- **Header Elements**:
  - Main Title: "RetailIQ"
  - Subtitle: "Executive Business Intelligence Dashboard"

### Visual Container Breakdown
1. **6 Top KPI Cards**:
   - `sales.Total Sales` (Card visual)
   - `sales.Total Profit` (Card visual)
   - `sales.Total Orders` (Card visual)
   - `sales.Total Quantity` (Card visual)
   - `sales.Profit Margin %` (Card visual)
   - `sales.Avg Shipping Days` (Card visual)
2. **Monthly Sales Trend (Line Chart)**:
   - X-Axis: `sales.Order Year`, `sales.Order Month`
   - Y-Axis: `sales.Total Sales`
3. **Sales by Category (Treemap)**:
   - Group: `sales.Category`
   - Details: `sales.Sub-Category`
   - Values: `sales.Total Sales`
4. **Profit by Market (Clustered Bar Chart)**:
   - Category / Y-Axis: `sales.Market`
   - Values / X-Axis: `sales.Total Profit`
5. **Top 10 Customers by Revenue (Clustered Bar Chart)**:
   - Category: `sales.Customer Name`
   - Values: `sales.Total Sales`
6. **Top 10 Products (Clustered Bar Chart)**:
   - Category: `sales.Product Name`
   - Values: `sales.Total Sales`
7. **Average Shipping Days by Ship Mode (Clustered Column Chart)**:
   - Category / X-Axis: `sales.Ship Mode`
   - Values / Y-Axis: `sales.Avg Shipping Days`
8. **Interactive Slicers**:
   - `sales.Order Year` (Multi-select / Dropdown)
   - `sales.Market` (Multi-select / Dropdown)
   - `sales.Category` (Multi-select / Dropdown)
   - `sales.Segment` (Multi-select / Dropdown)
9. **Action Button**: Configured for bookmark reset / clear filters.

---

## 7. Current Implementation Status

| File / Component | Status | Details |
|---|---|---|
| `data/Global_Superstore22.csv` | Complete | Raw transactional dataset (51,290 rows). Excluded from Git via `.gitignore`. |
| `data/cleaned_superstore.csv` | Complete | Generated output of cleaning script (51,290 rows × 28 cols). Excluded from Git. |
| `data/README.md` | Complete | Data setup instructions and schema documentation. |
| `python/01_data_profiling.py` | Complete | Standalone data profiling script with null/duplicate checks and distributions. |
| `python/02_data_cleaning.py` | Complete | Core cleaning, datetime normalization, and feature engineering script. |
| `python/03_feature_engineering.py` | Documented Stub | Architectural stub; logic lives inside `02_data_cleaning.py`. |
| `python/04_export_mysql.py` | Documented Stub | Architectural stub; ingestion pipeline lives inside `05_load_mysql.py`. |
| `python/05_load_mysql.py` | Complete | Secure SQLAlchemy ETL script using `.env` variables and PyMySQL. |
| `sql/01_create_database.sql` | Complete | `CREATE DATABASE IF NOT EXISTS retailiq; USE retailiq;` |
| `sql/02_business_queries.sql` | Complete | 10 verified business analytical SQL queries. |
| `powerbi/RetailIQ_Dashboard.pbix` | Complete | Pre-built executive dashboard with 19 visual containers and embedded model. |
| `reports/` | Complete | Directory initialized with `.gitkeep` for future exported PDF/Excel summaries. |
| `screenshots/` | Complete | Directory initialized with `.gitkeep` for dashboard visual previews. |
| `requirements.txt` | Complete | Contains `pandas`, `SQLAlchemy`, `PyMySQL`, `python-dotenv`. |
| `.env.example` | Complete | Template for MySQL connection parameters. |
| `.gitignore` | Complete | Standardized rules excluding cache, virtualenvs, credentials, and datasets. |
| `README.md` | Complete | Comprehensive portfolio and resume presentation document. |
| `CONTEXT.md` | Complete | Technical system specification (this document). |

---

## 8. Important Architectural & Project Decisions

1. **Feature Engineering Consolidated in `02_data_cleaning.py`**:
   - Rather than creating an intermediate CSV between cleaning and feature engineering, `Order Year`, `Order Month`, `Order Quarter`, `Shipping Days`, and `Profit Margin (%)` were generated directly inside `python/02_data_cleaning.py`. This ensures atomic generation of `cleaned_superstore.csv`.
2. **Environment Variable Decoupling in `05_load_mysql.py`**:
   - Database credentials (`DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME`) were abstracted into environment variables with `python-dotenv`. This protects against credential leaks when pushing to public repositories.
3. **Git Exclusion Strategy for Datasets**:
   - `data/cleaned_superstore.csv` (13.7 MB) is excluded because it is an unnecessary generated file that can be reproduced at any time via `python 02_data_cleaning.py`.
   - `data/Global_Superstore22.csv` (12.0 MB) is excluded from version control to comply with Git repository size best practices and avoid bloating the commit history with tabular data.
4. **Embedded Data Model in Power BI**:
   - The `.pbix` file contains the complete imported VertiPaq model. Reviewers do not need an active MySQL database running locally to open and evaluate the Power BI report.

---

## 9. Known Limitations

- **Historical Static Snapshot**: Dataset spans 2011 to 2014; no ongoing real-time API or webhook ingestion pipeline.
- **Relational Normalization**: The MySQL table `sales` is currently structured as a single denormalized analytical table (51,290 rows) rather than a normalized 3NF star schema (`dim_customer`, `dim_product`, `dim_geography`, `dim_date`, `fact_sales`).
- **Power BI Pages**: Single executive summary dashboard; secondary operational views (Customer Matrix, Shipping Deep-Dive) are planned for next iteration.

---

## 10. Future Development Roadmap

1. **Star Schema Data Modeling**:
   - Split denormalized `sales` table in MySQL into a formal Star Schema with dimension tables and a centralized fact table.
2. **Customer Segmentation (RFM Analysis)**:
   - Build a Python script computing Recency, Frequency, and Monetary (RFM) scores to categorize customers into Champions, Loyal, At-Risk, and Lost.
3. **Machine Learning Margin Predictor**:
   - Develop an XGBoost regression model predicting the likelihood of a transaction generating negative profit based on discount level, product category, and shipping mode.
4. **Power BI Visual Enhancements**:
   - Add drill-through pages for product sub-categories.
   - Embed visual screenshots in `screenshots/` and update README links.
