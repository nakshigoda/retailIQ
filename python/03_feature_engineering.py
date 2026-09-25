"""
RetailIQ - Feature Engineering
==============================
Note: In this implementation, feature engineering logic (Order Year, Order Month,
Order Quarter, Shipping Days, Profit Margin (%)) is executed directly within
`python/02_data_cleaning.py` to maintain a unified data cleaning and transformation pipeline.

Generated columns:
- Order Year: Extracted from Order Date (YYYY)
- Order Month: Extracted from Order Date (Month name)
- Order Quarter: Extracted from Order Date (Q1 - Q4)
- Shipping Days: Calculated as (Ship Date - Order Date) in days
- Profit Margin (%): Calculated as (Profit / Sales) * 100
"""
