# Data Directory

This directory stores the raw and processed datasets for RetailIQ.

### Datasets:
- **`Global_Superstore22.csv`** (Raw Dataset, ~12 MB): Primary transactional dataset with 51,290 records across 2011–2014. Excluded from Git to adhere to repository size best practices.
- **`cleaned_superstore.csv`** (Processed Dataset, ~13.7 MB): Generated artifact produced by executing `python python/02_data_cleaning.py`.

### How to Prepare Data:
1. Place `Global_Superstore22.csv` in this `data/` directory.
2. Run data cleaning and feature engineering:
   ```bash
   python python/02_data_cleaning.py
   ```
3. This creates `data/cleaned_superstore.csv`, ready for MySQL ingestion and Power BI loading.
