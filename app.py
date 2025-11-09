import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Mai Shan Yun Data Analysis")

orders = pd.read_csv("RestaurantData.csv")
ingredients = pd.read_csv("IngredientsUsed.csv")
shipments = pd.read_csv("MSY Data - Shipment.csv")

## INGREDIENT USAGE BY MONTH ##
# combines orders and ingredients into one table
usage = orders.merge(ingredients, on="Item name")

ingredient_cols = ingredients.columns.drop("Item name")  # all ingredient columns

# multiply each ingredient column by the Count of dishes sold
for col in ingredient_cols:
    usage[col] = usage[col] * usage["Count"]

months_in_data = ["May", "June", "July", "August", "September"]
usage["Month"] = pd.Categorical(
    usage["Month"],
    categories=months_in_data,
    ordered=True
)

monthly_totals = usage.groupby("Month")[ingredient_cols].sum().reset_index()
monthly_totals = monthly_totals.sort_values("Month")  # uses the categorical order


st.subheader("Ingredients used per month")
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



## Amount left ##
#shipment - quantity
shipments = pd.read_csv("MonthlyShipments.csv")

# Equate the files
ingredient_mapping = {
    "braised beef used (g)": "Beef",
    "Braised Chicken(g)": "Chicken",
    "Braised Pork(g)": "Pork",
    "Egg(count)": "Egg",
    "Rice(g)": "Rice",
    "Ramen (count)": "Ramen",
    "Rice Noodles(g)": "Rice Noodles",
    "chicken thigh (pcs)": "Chicken Thigh",
    "Chicken Wings (pcs)": "Chicken Wings",
    "flour (g)": "Flour",
    "Pickle Cabbage": "Pickle Cabbage",
    "Green Onion": "Green Onion",
    "Cilantro": "Cilantro",
    "White onion": "White Onion",
    "Peas(g)": "Peas + Carrot",
    "Carrot(g)": "Peas + Carrot",
    "Boychoy(g)": "Bokchoy",
    "Tapioca Starch": "Tapioca Starch"
}

# Rename columns
ingredients_renamed = ingredients.rename(columns=ingredient_mapping)

# Combine Peas + Carrot into one column
ingredients_renamed["Peas + Carrot"] = (
    ingredients_renamed[["Peas + Carrot", "Peas + Carrot"]].sum(axis=1)
)

# Melt into long format: Item name, Ingredient, AmountUsed
ingredients_long = ingredients_renamed.melt(
    id_vars="Item name",
    value_vars=ingredients_renamed.columns[1:],  # all ingredient columns
    var_name="Ingredient",
    value_name="AmountUsed"
)

# Pivot so ingredients are rows and items are columns
ingredients_pivot = ingredients_long.pivot_table(
    index="Ingredient",
    columns="Item name",
    values="AmountUsed",
    aggfunc="sum"  # combine duplicates like Peas + Carrot
).reset_index()

# Load shipments
shipments = pd.read_csv("MonthlyShipments.csv")
shipments.columns = shipments.columns.str.strip()
shipment_dict = dict(zip(shipments["Ingredient"], shipments["quantity"]))

# Add shipment quantity column
ingredients_pivot["Shipment Quantity"] = ingredients_pivot["Ingredient"].map(shipment_dict)

# Streamlit display
st.subheader("Ingredient Usage by Item")
st.dataframe(ingredients_pivot)
import plotly.express as px

# ingredients_pivot: rows = ingredients, columns = items
fig = px.imshow(
    ingredients_pivot.drop(columns=["Shipment Quantity","TotalUsed","StockRemaining"]), 
    labels=dict(x="Menu Item", y="Ingredient", color="Usage (g)"),
    color_continuous_scale="Viridis"
)
st.plotly_chart(fig)



