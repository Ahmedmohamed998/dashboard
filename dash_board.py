import pandas as pd
import plotly.express as px
import numpy as np
import streamlit as st
st.set_page_config(page_title="Churn Modelling Dashboard", layout="wide")
st.title("Churn Modelling Dashboard")
@st.cache_data
def df_get_from_csv():
    df = pd.read_csv("Churn_Modelling.csv")
    return df
df=df_get_from_csv()
df.head()
df.isnull().sum()
#drop null because it is too small
df.dropna(inplace=True)
df.duplicated().sum()
#drop dublicates
df.drop_duplicates(inplace=True)
df['joining_year']=2024-df['Tenure']
# Streamlit app
# side bar
st.sidebar.header("please filter here:")
gender=st.sidebar.multiselect("select gender",options=df['Gender'].unique(),default=df['Gender'].unique())
year=st.sidebar.multiselect("select year",options=df['joining_year'].unique(),default=df['joining_year'].unique())
exited=st.sidebar.multiselect("select if custmoer exited or not ",options=df['Exited'].unique(),default=df['Exited'].unique())
df=df.query('Gender==@gender & joining_year==@year & Exited==@exited')
# Create a layout with columns
col1, col2 = st.columns([2, 2])

# Gender Distribution Pie Chart
with col1:
    st.subheader("Gender Distribution")
    fig = px.pie(df, names='Gender', title="Gender Distribution", color_discrete_sequence=['blue', 'pink'])
    st.plotly_chart(fig)
    with st.expander("Insights"):
        st.write("""
            - Approximately 54.6% of the customers are male.
        """)

# Age Distribution Histogram
with col2:
    st.subheader("Age Distribution")
    fig = px.histogram(df, x='Age', title="Age Distribution", color_discrete_sequence=['blue'])
    fig.update_traces(marker=dict(line=dict(color='black', width=2)))
    st.plotly_chart(fig)
    with st.expander("Insights"):
        st.write("""
            - The average age of customers is around 38.13 years..
        """)

# Active Member Distribution Pie Chart
with col1:
    st.subheader("Active Member Distribution")
    fig = px.pie(df, names='IsActiveMember', title="IsActiveMember Distribution", color_discrete_sequence=['red', 'black'])
    st.plotly_chart(fig)
    with st.expander("Insights"):
        st.write("""
            - Approximately 51.5% of customers are active members (IsActiveMember).
        """)
# Geography Distribution Bar Chart
with col2:
    st.subheader("Geography Distribution")
    geo_counts = df['Geography'].value_counts().reset_index()
    geo_counts.columns = ['Geography', 'Count']
    fig = px.bar(geo_counts, y='Geography', x='Count', title="Geography Distribution", color='Geography', color_discrete_sequence=['lightblue', 'blue', 'purple'])
    st.plotly_chart(fig)
    with st.expander("Insights"):
        st.write("""
            - The majority of our customers are form france
        """)

# Credit Card Ownership Bar Chart
with col1:
    st.subheader("Credit Ownership Distribution")
    credit = df['HasCrCard'].value_counts().reset_index()
    credit.columns = ['status', 'count']
    fig = px.bar(credit, y='count', x='status', title='Has Credit Card Distribution', color_discrete_sequence=['red', 'lightred'])
    st.plotly_chart(fig)
    with st.expander("Insights"):
        st.write("""
            - A significant proportion (around 75.4%) of customers have a credit card (HasCrCard).
        """)

# credit card score Distribution Histogram
with col2:
    st.subheader("CreditScore")
    fig = px.histogram(df, x='CreditScore', title="CreditScore", color_discrete_sequence=['blue'])
    fig.update_traces(marker=dict(line=dict(color='black', width=2)))
    st.plotly_chart(fig)
    with st.expander("Insights"):
        st.write("""
            - The average credit score is approximately 656.45.
            - The minimum credit score is 350, and the maximum is 850.
        """)


# Exited Customers Bar Chart
with col1:
    st.subheader("Exited Customers Distribution")
    Exited = df['Exited'].value_counts().reset_index()
    Exited.columns = ['status', 'count']
    fig = px.bar(Exited, y='count', x='status', title='Exited Customers Distribution', color_discrete_sequence=['blue'])
    st.plotly_chart(fig)
    with st.expander("Insights"):
        st.write("""
            - About 21.2% of customers have exited the bank (Exited = 1).
            - The majority (about 78.8%) have not exited the bank (Exited = 0).
        """)

# Joining Year Line Chart
with col2:
    st.subheader("Joining Year Distribution")
    df['joining_year'] = 2024 - df['Tenure']
    year = df['joining_year'].value_counts().reset_index()
    year.columns = ['joining_year', 'Count']
    year = year.sort_values(by='joining_year')
    fig = px.line(year, x='joining_year', y='Count', title="Joining Year Distribution", color_discrete_sequence=['red'])
    st.plotly_chart(fig)
    with st.expander("Insights"):
        st.write("""
            - The year 2023 saw the highest number of customers, totaling 1035.
            - Conversely, 2024 had the lowest number of customers, with only 415.
            - On average, we attract around 1000 customers each year.
        """)
