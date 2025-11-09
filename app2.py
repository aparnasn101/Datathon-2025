##Top 5 Most popular dishes
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

c1,c2,c3 = st.columns([1,2,1])
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

            #st.write("May:")
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
            
            #st.write("June:")
            df_sorted = df.sort_values(by='Count',ascending=False)
            top = df_sorted.head(5)
            #st.dataframe(df_sorted)  
            #st.pyplot(df_sorted['Count'].plot(kind='pie',autopct='%1.1f%%').figure) 
            fig,ax = plt.subplots()
            ax.bar(top['Item Name'],top['Count'],color='red')
            ax.set_xlabel('Dishes')
            ax.set_ylabel('Amount Ordered')
            ax.set_title("June")
            st.pyplot(fig)

    elif graph_option == 'July':
        July = 'JulyDishes.csv'
        if July is not None:
            df = pd.read_csv(July)
            #st.write("July:")

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
            #st.write("August:")

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
            #st.write("September:")

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
            #st.write("October:")

            df_sorted = df.sort_values(by='Count',ascending=False)
            top = df_sorted.head(5)
            fig,ax = plt.subplots()
            ax.bar(top['Item Name'],top['Count'],color='skyblue')
            ax.set_xlabel('Dishes')
            ax.set_ylabel('Amount Ordered')
            ax.set_title("October")
            st.pyplot(fig)


   

            

