import pandas as pd

# Load dataset
df = pd.read_csv("../data/Global_Superstore22.csv", encoding="latin1")

print("Dataset Loaded Successfully!")

# -----------------------------
# Convert Date Columns
# -----------------------------
df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    dayfirst=True
)

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"],
    dayfirst=True
)

# -----------------------------
# Remove Extra Spaces
# -----------------------------
text_columns = df.select_dtypes(include=["string", "object"]).columns

for col in text_columns:
    df[col] = df[col].str.strip()

# -----------------------------
# Feature Engineering
# -----------------------------

df["Order Year"] = df["Order Date"].dt.year

df["Order Month"] = df["Order Date"].dt.month_name()

df["Order Quarter"] = df["Order Date"].dt.quarter

df["Shipping Days"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

df["Profit Margin (%)"] = (
    df["Profit"] / df["Sales"]
) * 100

print("\n========== DATA QUALITY REPORT ==========")

print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

print(f"\nMissing Values: {df.isnull().sum().sum()}")

print(f"Duplicate Rows: {df.duplicated().sum()}")

print(f"\nNegative Profit Orders: {(df['Profit'] < 0).sum()}")

print(f"Zero Profit Orders: {(df['Profit'] == 0).sum()}")

print(f"\nAverage Shipping Days: {df['Shipping Days'].mean():.2f}")

print(f"Average Discount: {df['Discount'].mean():.2f}")

print(f"Average Profit Margin: {df['Profit Margin (%)'].mean():.2f}%")

# -----------------------------
# Save Clean Dataset
# -----------------------------
df.to_csv("../data/cleaned_superstore.csv", index=False)

print("\nCleaning Completed Successfully!")

print("\nNew Columns Added:")
print(df.columns)

print("\nPreview:")
print(df.head())