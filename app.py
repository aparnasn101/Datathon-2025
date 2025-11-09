import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import calendar

st.set_page_config(page_title="Mai Shan Yun Data Analysis", layout="wide")
st.title("Mai Shan Yun Data Analysis")

# ------------------------------
# 1) LOAD CSVs
# ------------------------------
orders = pd.read_csv("Restaurant Data.csv", thousands=',')
ingredients = pd.read_csv("IngredientsUsed.csv", thousands=',')
shipments = pd.read_csv("MSY Data - Shipment.csv")  # not used yet, but loaded

# Explicit month order
months_in_data = ["May", "June", "July", "August", "September", "October"]
orders["Month"] = pd.Categorical(orders["Month"], categories=months_in_data, ordered=True)

# ------------------------------
# 3) MERGE ORDERS WITH INGREDIENT RECIPES
#    (LEFT JOIN so October stays even if items don't match)
# ------------------------------
if "Item Name" not in orders.columns:
    st.error("Orders missing 'Item Name'. Columns: " + ", ".join(orders.columns))
if "Item Name" not in ingredients.columns:
    st.error("Ingredients missing 'Item Name'. Columns: " + ", ".join(ingredients.columns))

usage = orders.merge(ingredients, on="Item Name", how="left", indicator=True)

# Ingredient columns are everything from ingredients except the key
ingredient_cols = [c for c in ingredients.columns if c != "Item Name"]


# ------------------------------
# 5) BUILD INGREDIENT USAGE
# ------------------------------
# Coerce each ingredient column to numeric and multiply by dish count
for col in ingredient_cols:
    usage[col] = pd.to_numeric(usage[col], errors="coerce").fillna(0)
    usage[col] = usage[col] * usage["Count"]

# Monthly totals across all ingredients
monthly_totals = usage.groupby("Month", as_index=False)[ingredient_cols].sum()

# OPTIONAL: Drop columns that are all zeros across all months (keeps visuals cleaner)
drop_zero_only = True
if drop_zero_only:
    monthly_totals = monthly_totals.loc[:, (monthly_totals != 0).any(axis=0)]

# After dropping zero-only columns, recompute the list we will use everywhere
valid_cols = [c for c in ingredient_cols if c in monthly_totals.columns]

# ------------------------------
# 6) SHOW TABLE: INGREDIENTS USED PER MONTH
# ------------------------------
st.subheader("Ingredients Used per Month")
if len(valid_cols) == 0:
    st.warning("No ingredient columns with non-zero totals. Likely because many items (esp. October) use category names with no recipe match. Add recipes or a mapping for those items.")
else:
    st.dataframe(monthly_totals)

# ------------------------------
# 7) HEATMAP: ABSOLUTE USAGE
# ------------------------------
if len(valid_cols) > 0:
    heatmap_data = monthly_totals.set_index("Month")[valid_cols]
    fig = px.imshow(
        heatmap_data.T,
        labels=dict(x="Month", y="Ingredient", color="Usage"),
        title="Ingredient Usage Heatmap",
        aspect="auto"
    )
    st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# 8) HEATMAP: PERCENT DISTRIBUTION ACROSS MONTHS
# ------------------------------
if len(valid_cols) > 0:
    ingredient_pct = monthly_totals.copy()
    # Avoid divide-by-zero: if a column sums to zero, keep it zero
    sums = ingredient_pct[valid_cols].sum(axis=0).replace({0: np.nan})
    ingredient_pct[valid_cols] = ingredient_pct[valid_cols].div(sums, axis=1) * 100
    ingredient_pct[valid_cols] = ingredient_pct[valid_cols].fillna(0)

    heatmap_pct = ingredient_pct.set_index("Month")[valid_cols]
    fig2 = px.imshow(
        heatmap_pct.T,
        labels=dict(x="Month", y="Ingredient", color="% of Total Usage"),
        title="Ingredient Usage Spread Across Months",
        aspect="auto",
        text_auto=True
    )
    st.plotly_chart(fig2, use_container_width=True)

# ------------------------------
# 9) SIMPLE LINEAR PROJECTIONS (NEXT 3 MONTHS)
# ------------------------------
st.subheader("Predicted Ingredient Usage for Next 3 Months")
if len(valid_cols) == 0:
    st.info("No valid ingredient columns to predict. Add recipe mappings for unmatched items to enable predictions.")
else:
    # Build a 3-row frame (future months) and fill each ingredient as a column
    future_index = ["Next Month 1", "Next Month 2", "Next Month 3"]  # 3 rows
    predictions = pd.DataFrame(index=future_index, columns=valid_cols, dtype=float)  # columns = ingredients

    # Use month index positions 0..N-1 for regression
    X = np.arange(len(monthly_totals)).reshape(-1, 1)

    for col in valid_cols:
        y = monthly_totals[col].values
        # If y is all zeros, the model is degenerate; keep zeros
        if np.allclose(y, 0):
            pred = np.array([0.0, 0.0, 0.0])
        else:
            model = LinearRegression()
            model.fit(X, y)
            X_future = np.arange(len(monthly_totals), len(monthly_totals) + 3).reshape(-1, 1)
            pred = np.round(model.predict(X_future), 1)
        predictions[col] = pred  # assign 3 values to the 3-row frame

    st.dataframe(predictions.T)  # rows = ingredients, cols = future months

##

c1,c2 = st.columns([1,3])
#Creates buttons to switch through months
with c1:
    st.markdown("Top Dishes Per Month")
    graph_option = st.radio(
        "Select Month",
        ('May','June','July','August','September','October')
    )
with c2:
    
    if graph_option == 'May':
        May = 'MayDishes.csv'
        if May is not None:
            df = pd.read_csv(May)

            df_sorted = df.sort_values(by='Count',ascending=False) #orders them
            top = df_sorted.head(5) #takes the top 3 for the graph
            fig,ax = plt.subplots()
            ax.bar(top['Item Name'],top['Count'],color='skyblue')
            ax.set_xlabel('Dishes')
            ax.set_ylabel('Amount Ordered')
            ax.set_title("May")
            st.pyplot(fig)

    elif graph_option == 'June':
        June = 'JuneDishes.csv'
        if June is not None:
            df = pd.read_csv(June)
            
     
            df_sorted = df.sort_values(by='Count',ascending=False)
            top = df_sorted.head(5) 
            fig,ax = plt.subplots()
            ax.bar(top['Item Name'],top['Count'],color='skyblue')
            ax.set_xlabel('Dishes')
            ax.set_ylabel('Amount Ordered')
            ax.set_title("June")
            st.pyplot(fig)

    elif graph_option == 'July':
        July = 'JulyDishes.csv'
        if July is not None:
            df = pd.read_csv(July)
    

            df_sorted = df.sort_values(by='Count',ascending=False)
            top = df_sorted.head(5)
            fig,ax = plt.subplots()
            ax.bar(top['Item Name'],top['Count'],color='skyblue')
            ax.set_xlabel('Dishes')
            ax.set_ylabel('Amount Ordered')
            ax.set_title("July")
            st.pyplot(fig)

    elif graph_option == 'August':
        August = 'AugustDishes.csv'
        if August is not None:
            df = pd.read_csv(August)
     

            df_sorted = df.sort_values(by='Count',ascending=False)
            top = df_sorted.head(5)
            fig,ax = plt.subplots()
            ax.bar(top['Item Name'],top['Count'],color='skyblue')
            ax.set_xlabel('Dishes')
            ax.set_ylabel('Amount Ordered')
            ax.set_title("August")
            st.pyplot(fig)

    elif graph_option == 'September':
        September = 'SeptemberDishes.csv'
        if September is not None:
            df = pd.read_csv(September)
           

            df_sorted = df.sort_values(by='Count',ascending=False)
            top = df_sorted.head(5)
            fig,ax = plt.subplots()
            ax.bar(top['Item Name'],top['Count'],color='skyblue')
            ax.set_xlabel('Dishes')
            ax.set_ylabel('Amount Ordered')
            ax.set_title("September")
            st.pyplot(fig)

    elif graph_option == 'October':
        October = 'OctoberDishes.csv'
        if October is not None:
            df = pd.read_csv(October)
          

            df_sorted = df.sort_values(by='Count',ascending=False)
            top = df_sorted.head(5)
            fig,ax = plt.subplots()
            ax.bar(top['Item Name'],top['Count'],color='skyblue')
            ax.set_xlabel('Dishes')
            ax.set_ylabel('Amount Ordered')
            ax.set_title("October")
            st.pyplot(fig)


   

            

