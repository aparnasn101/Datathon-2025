import pandas as pd
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

# -----------------------------
# CONFIGURATION
# -----------------------------

# Path to your Excel file
file_path = "May.xlsx"  # change this to whatever file exists

# Usual counts per ingredient (adjust as needed)
usual_counts = {
    "Beef": 200,
    "Chicken": 200,
    "Shrimp": 100,
    # Add more items here
}

# Alert threshold (fraction of usual stock)
threshold_factor = 0.25  # alert if count <= 25% of usual

# -----------------------------
# LOAD DATA
# -----------------------------

if not Path(file_path).exists():
    print(f"File {file_path} not found.")
    exit()

df = pd.read_excel(file_path)

# Normalize column names
df.columns = [str(c).strip().lower() for c in df.columns]

# Try to find 'item' and 'count' columns
item_col = next((c for c in df.columns if "item" in c), None)
count_col = next((c for c in df.columns if "count" in c or "qty" in c or "quantity" in c), None)

if not item_col or not count_col:
    print("Cannot find 'item' or 'count' columns in your file.")
    exit()

df[item_col] = df[item_col].astype(str).str.strip()
df[count_col] = pd.to_numeric(df[count_col], errors="coerce").fillna(0)

# -----------------------------
# CHECK LOW STOCK
# -----------------------------

low_alerts = []

for _, row in df.iterrows():
    item = row[item_col]
    count = row[count_col]
    usual = usual_counts.get(item, 100)  # default 100 if unknown
    threshold = usual * threshold_factor
    if count <= threshold:
        low_alerts.append(f"{item}: {count} left (Restock soon!)")

# -----------------------------
# SHOW POP-UP ALERTS
# -----------------------------

if low_alerts:
    root = tk.Tk()
    root.withdraw()  # hide main window
    message = "\n".join(low_alerts)
    messagebox.showwarning("Low Stock Alert!", message)
else:
    print("All ingredients above threshold ✅")
