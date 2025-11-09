# Datathon-2025
# Challenge - Mai Shan Yun

An interactive **Streamlit dashboard** for analyzing ingredient usage, monthly trends, and forecasting future demand for Mai Shan Yun’s restaurant operations.

# Mai Shan Yun Data Analysis Dashboard

An interactive **Streamlit dashboard** for analyzing ingredient usage, monthly trends, and forecasting future demand for Mai Shan Yun’s restaurant operations.

---

## Overview

This project combines restaurant order data, ingredient usage, and shipment records to visualize how ingredients are consumed over time and predict future usage using linear regression.

The dashboard provides:
- **Monthly ingredient consumption analysis**
- **Heatmaps** of ingredient usage
- **Percentage spread** of each ingredient across months
- **Forecasts** for ingredient demand in upcoming months
- **Graphs** 

Built for **Mai Shan Yun** as part of a data analysis project for TAMU Datathon 2025.

---

## Features

- **Automatic data merging** between orders and ingredients  
- **Month-by-month breakdown** of ingredient usage  
- **Interactive heatmaps** (Plotly)  
- **Static and custom visualizations** (Matplotlib)   
- **Handles messy CSV data** (missing values, text formatting, commas in numbers)

---

## Tech Stack

| Component | Technology |
|------------|-------------|
| Dashboard | [Streamlit](https://streamlit.io/) |
| Data Analysis | [pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/) |
| Visualization | [Plotly Express](https://plotly.com/python/plotly-express/), [Matplotlib](https://matplotlib.org/) |
| Forecasting | [scikit-learn (LinearRegression)](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html) |

---

## Data Files

We used the following data files to create new files to be used for the dashboard:
| File |
|---------------|
| `August_Data_Matrix (1).xlsx` |
| `July_Data_Matrix (1).xlsx` |
| `June_Data_Matrix.xlsx` |
| `MSY Data - Ingredient.csv` |
| `MSY Data - Shipment.csv` |
| `May_Data_Matrix (1).xlsx` |
| `October_Data_Matrix_20251103_214000.xlsx` |
| `September_Data_Matrix.xlsx` |

We condensed this data into the following files that we used for the dashboard:
| File | Description |
|------|--------------|
| `Restaurant Data.csv` | Contains order data for each month (Item Name, Count, Month, etc.) |
| `IngredientsUsed.csv` | Maps each menu item to the ingredients used |
| `MSY Data - Shipment.csv` | Shipment and stock data (not yet visualized in this version) |
| `MonthlyShipments.csv` | Converts the shipments given to determine the monthly stock received |
| `MayDishes.csv` | Data for the dishes ordered in May |
| `JuneDishes.csv` | Data for the dishes ordered in June |
| `JulyDishes.csv` | Data for the dishes ordered in July |
| `AugustDishes.csv` | Data for the dishes ordered in August |
| `SeptemberDishes.csv` | Data for the dishes ordered in September |
| `OctoberDishes.csv` | Data for the dishes ordered in October |

Make sure these files are placed in the same directory as `app.py`, `app2.py`, and `low_ingredients_alert.py`.

---


