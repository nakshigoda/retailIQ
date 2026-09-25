import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# -----------------------------
# MySQL Credentials
# -----------------------------
USERNAME = os.getenv("DB_USER", "root")
PASSWORD = os.getenv("DB_PASSWORD", "")
HOST = os.getenv("DB_HOST", "localhost")
PORT = os.getenv("DB_PORT", "3306")
DATABASE = os.getenv("DB_NAME", "retailiq")

# -----------------------------
# Connect to MySQL
# -----------------------------
engine = create_engine(
    f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
)

print("Connected to MySQL!")

# -----------------------------
# Read Cleaned Dataset
# -----------------------------
df = pd.read_csv("../data/cleaned_superstore.csv")

print("Dataset Loaded!")

# -----------------------------
# Upload to MySQL
# -----------------------------
df.to_sql(
    "sales",
    con=engine,
    if_exists="replace",
    index=False
)

print("Table 'sales' created successfully!")
print(f"Rows inserted: {len(df)}")