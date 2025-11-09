import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

st.title("Mai Shan Yun Data Analysis")

orders = pd.read_csv("Restaurant Data.csv", thousands=',')
ingredients = pd.read_csv("IngredientsUsed.csv", thousands=',')
shipments = pd.read_csv("MSY Data - Shipment.csv")

## INGREDIENT USAGE BY MONTH ##
# combines orders and ingredients into one table
usage = orders.merge(ingredients, on="Item Name")

ingredient_cols = ingredients.columns.drop("Item Name")  # all ingredient columns

# multiply each ingredient column by the Count of dishes sold
# Ensure Count column is numeric
usage["Count"] = pd.to_numeric(usage["Count"], errors="coerce").fillna(0)

# Convert all ingredient columns to numeric
for col in ingredient_cols:
    usage[col] = usage[col] * usage["Count"]


# months_in_data = ["May", "June", "July", "August", "September", "October"]
# usage["Month"] = pd.Categorical(
#     usage["Month"],
#     categories=months_in_data,
#     ordered=True
# )
st.write("Unique month values:", usage["Month"].unique())


monthly_totals = usage.groupby("Month")[ingredient_cols].sum().reset_index()
monthly_totals = monthly_totals.sort_values("Month")  # uses the categorical order


st.subheader("Ingredients used per month")
monthly_totals = monthly_totals.loc[:, (monthly_totals != 0).any(axis=0)]
st.dataframe(monthly_totals)


# Heatmap
heatmap_data = monthly_totals.set_index("Month")[ingredient_cols]
fig = px.imshow(
    heatmap_data.T,
    labels=dict(x="Month", y="Ingredient", color="Usage"),
    title="Ingredient Usage Heatmap",
    aspect="auto"
)
st.plotly_chart(fig)


# Ingredient spread across months
ingredient_pct = monthly_totals.copy()

# Divide each ingredient column by its total across all months
ingredient_pct[ingredient_cols] = ingredient_pct[ingredient_cols].div(
    ingredient_pct[ingredient_cols].sum(axis=0), axis=1
) * 100

# Now each column sums to 100% (distribution of that ingredient across months)
heatmap_data = ingredient_pct.set_index("Month")[ingredient_cols]

fig = px.imshow(
    heatmap_data.T,
    labels=dict(x="Month", y="Ingredient", color="% of Total Usage"),
    title="Ingredient Usage Spread Across Months",
    aspect="auto",
    text_auto=True
)
st.plotly_chart(fig)

predictions = pd.DataFrame({"Ingredient": ingredient_cols})

for col in ingredient_cols:
    y = monthly_totals[col].values
    X = np.arange(len(monthly_totals)).reshape(-1,1)  # 0,1,2,... for months
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict next 3 months
    X_future = np.arange(len(monthly_totals), len(monthly_totals)+3).reshape(-1,1)
    pred = model.predict(X_future)
    
    predictions[col] = np.round(pred, 1)

predictions.index = ["Next Month 1", "Next Month 2", "Next Month 3"]
st.subheader("Predicted Ingredient Usage for Next 3 Months")
st.dataframe(predictions.T)















