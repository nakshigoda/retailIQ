import pandas as pd

# ==============================
# STEP 1: Load the Dataset
# ==============================

df = pd.read_csv("../data/Global_Superstore22.csv", encoding="latin1")

print("=" * 50)
print("DATASET LOADED SUCCESSFULLY")
print("=" * 50)

# ==============================
# STEP 2: Basic Information
# ==============================

print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)

# ==============================
# STEP 3: First & Last Records
# ==============================

print("\nFirst 5 Rows:")
print(df.head())

print("\nLast 5 Rows:")
print(df.tail())

# ==============================
# STEP 4: Missing Values
# ==============================

print("\nMissing Values:")
print(df.isnull().sum())

# ==============================
# STEP 5: Duplicate Records
# ==============================

duplicates = df.duplicated().sum()

print("\nDuplicate Rows:")
print(duplicates)

# ==============================
# STEP 6: Numerical Summary
# ==============================

print("\nStatistical Summary:")
print(df.describe())

# ==============================
# STEP 7: Unique Values
# ==============================

print("\nUnique Countries:")
print(df["Country"].nunique())

print("\nUnique Categories:")
print(df["Category"].unique())

print("\nUnique Segments:")
print(df["Segment"].unique())

print("\nUnique Ship Modes:")
print(df["Ship Mode"].unique())

print("\nUnique Markets:")
print(df["Market"].unique())

print("\nData Profiling Completed Successfully!")