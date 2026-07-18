import os
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "formatted_data.csv")

files = [
    "daily_sales_data_0.csv",
    "daily_sales_data_1.csv",
    "daily_sales_data_2.csv"
]

dfs = []

for file in files:
    path = os.path.join(DATA_DIR, file)

    df = pd.read_csv(path)


    df = df[df["product"].str.lower().str.strip() == "pink morsel"]

    
    df["price"] = (
        df["price"]
        .str.replace("$", "", regex=False)
        .astype(float)
    )

    # Calculate sales
    df["sales"] = df["price"] * df["quantity"]

    # Keep only required columns
    df = df[["sales", "date", "region"]]

    dfs.append(df)

# Combine all files
final_df = pd.concat(dfs, ignore_index=True)

# Save output
final_df.to_csv(OUTPUT_FILE, index=False)

print(" saved successfully!")
print(final_df.head())