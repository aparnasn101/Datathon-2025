import pandas as pd
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

# -----------------------------
# CONFIGURATION
# -----------------------------
# Your friend's file names for each month
may_file = "May.xlsx"
jun_file = "June.xlsx"
jul_file = "July.xlsx"
aug_file = "August.xlsx"
sep_file = "September.xlsx"
oct_file = "October.xlsx"

all_files = [may_file, jun_file, jul_file, aug_file, sep_file, oct_file]

threshold_factor = 0.25  # alert if count <= 25% of usual

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def normalize_columns(df):
    import re
    cols_map = {}
    for c in df.columns:
        key = re.sub(r'[^a-z0-9]', ' ', str(c).lower()).strip()
        if "item" in key and "name" in key:
            cols_map[c] = "item"
        elif key in ("category", "item", "item name", "name"):
            cols_map[c] = "item"
        elif "count" in key or "qty" in key or "quantity" in key:
            cols_map[c] = "count"
        elif "amount" in key or "price" in key or "total" in key or "$" in key:
            cols_map[c] = "amount"
        else:
            cols_map[c] = c
    return df.rename(columns=cols_map)

def clean_numeric_series(s):
    if s.dtype == object:
        s = s.astype(str).str.replace(r'[^0-9.\-]', '', regex=True)
    return pd.to_numeric(s, errors='coerce').fillna(0)

def load_file_sheets(file_path):
    """Return a list of DataFrames from all sheets (for Excel) or single DF (for CSV)."""
    file_path = Path(file_path)
    if not file_path.exists():
        return []
    if file_path.suffix.lower() in [".xlsx", ".xls"]:
        xls = pd.ExcelFile(file_path)
        return [pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names]
    elif file_path.suffix.lower() == ".csv":
        return [pd.read_csv(file_path)]
    else:
        return []

# -----------------------------
# PROCESS FILES
# -----------------------------
all_low_alerts = []

for file_path in all_files:
    sheets = load_file_sheets(file_path)
    if not sheets:
        print(f"No valid sheets found in {file_path}")
        continue

    for sheet_df in sheets:
        df = normalize_columns(sheet_df)

        # Find item and count columns
        item_col = next((c for c in df.columns if "item" in c), None)
        count_col = next((c for c in df.columns if "count" in c or "qty" in c or "quantity" in c), None)

        if not item_col or not count_col:
            continue

        df[item_col] = df[item_col].astype(str).str.strip()
        df[count_col] = clean_numeric_series(df[count_col])

        # Calculate "usual stock" as the **average count per ingredient**
        usual_counts = df.groupby(item_col)[count_col].mean().to_dict()

        # Check low stock
        for _, row in df.iterrows():
            item = row[item_col]
            count = row[count_col]
            usual = usual_counts.get(item, 100)
            threshold = usual * threshold_factor
            if count <= threshold:
                all_low_alerts.append(f"{item}: {count} left in {Path(file_path).name} (Restock soon!)")

# -----------------------------
# SHOW POP-UP ALERTS
# -----------------------------
if all_low_alerts:
    root = tk.Tk()
    root.withdraw()  # hide main window
    message = "\n".join(all_low_alerts)
    messagebox.showwarning("Low Stock Alert!", message)
else:
    print("All ingredients above threshold ✅")

