import pandas as pd
import os

def load_data():
    filename = "Database with pivot tables.xlsx"

    if not os.path.exists(filename):
        raise FileNotFoundError(f"{filename} not found in project root.")

    xls = pd.ExcelFile(filename)
    first_sheet = xls.sheet_names[0]

    df = pd.read_excel(filename, sheet_name=first_sheet)

    required_cols = [
        "property", "utility", "provider_code", "meter_number",
        "start_date", "end_date", "usage", "cost", "occupancy"
    ]

    for col in required_cols:
        if col not in df.columns:
            df[col] = None

    df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce")
    df["end_date"] = pd.to_datetime(df["end_date"], errors="coerce")

    df["year"] = df["start_date"].dt.year
    df["month"] = df["start_date"].dt.month

    return df
