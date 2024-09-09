import pandas as pd
import plotly.express as px
import numpy as np
import streamlit as st
st.set_page_config(page_title="Churn Modelling Dashboard", layout="wide")
st.title("Churn Modelling Dashboard")
@st.cache_data
def df_get_from_csv():
    df = pd.read_csv("Bank.csv")
    return df
df=df_get_from_csv()
df.duplicated().sum()
#drop dublicates
df.drop_duplicates(inplace=True)
df['joining_year']=2024-df['Tenure']
# Streamlit app
# Side bar
st.sidebar.header("Please filter here:")
gender = st.sidebar.multiselect("Select Gender", options=df['Gender'].unique(), default=df['Gender'].unique())
year = st.sidebar.multiselect("Select Year", options=df['joining_year'].unique(), default=df['joining_year'].unique())
exited = st.sidebar.multiselect("Select if customer exited or not", options=df['Exited'].unique(), default=df['Exited'].unique())
df = df.query('Gender==@gender & joining_year==@year & Exited==@exited')

# Create a layout with three columns
col1, col2, col3 = st.columns([2, 2, 2])

# Gender Distribution Pie Chart
with col1:
    st.subheader("Gender Distribution")
    fig = px.pie(df, names='Gender', title="Gender Distribution", color_discrete_sequence=['blue', 'pink'])
    st.plotly_chart(fig)
    with st.expander("Insights"):
        st.write("""
            - Approximately 56.4% of the customers are male.
        """)

# Age Distribution Histogram
with col2:
    st.subheader("Age Distribution")
    fig = px.histogram(df, x='Age', title="Age Distribution", color_discrete_sequence=['blue'])
    fig.update_traces(marker=dict(line=dict(color='blue', width=2)))
    st.plotly_chart(fig)
    with st.expander("Insights"):
        st.write("""
            - The average age of customers is around 38.13 years.
        """)
# Churnde customers by age group
with col3:
    st.subheader("Churnde customers by age group")
    age_bins = [18, 30, 40, 50, 60, 70, 80]
    age_labels = ['18-30', '31-40', '41-50', '51-60', '61-70', '71-80']
    df['AgeGroup'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels, right=False)
    churn_count = df[df['Exited'] == 1].groupby('AgeGroup')['Exited'].count().reset_index()
    fig = px.bar(churn_count, x='AgeGroup', y='Exited',title='Number of Churned Customers by Age Group',labels={'Exited': 'Number of Churned Customers', 'AgeGroup': 'Age Group'},height=450,color_discrete_sequence=['red'])
    st.plotly_chart(fig)
    with st.expander("Insights"):
        st.write("""
           - Most customers who churned are between the ages of 41 and 50.
        """)
# Geography Distribution Bar Chart
with col1:
    st.subheader("Geography Distribution")
    geo_counts = df['Geography'].value_counts().reset_index()
    geo_counts.columns = ['Geography', 'Count']
    fig = px.bar(geo_counts, y='Geography', x='Count', title="Geography Distribution", color='Geography', color_discrete_sequence=['lightblue', 'blue', 'purple'])
    st.plotly_chart(fig)
    with st.expander("Insights"):
        st.write("""
            - The majority of our customers are from France.
        """)

# Credit Card Ownership Bar Chart
with col2:
    st.subheader("Credit Card Ownership Distribution")
    credit = df['HasCrCard'].value_counts().reset_index()
    credit.columns = ['Status', 'Count']
    fig = px.bar(credit, y='Count', x='Status', title='Has Credit Card Distribution', color_discrete_sequence=['red', 'lightred'])
    st.plotly_chart(fig)
    with st.expander("Insights"):
        st.write("""
            - A significant proportion (around 75.4%) of customers have a credit card (HasCrCard).
        """)

# Credit Score Distribution Histogram
with col3:
    st.subheader("Credit Score Distribution")
    fig = px.histogram(df, x='CreditScore', title="Credit Score Distribution", color_discrete_sequence=['blue'])
    fig.update_traces(marker=dict(line=dict(color='blue', width=2)))
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
    Exited.columns = ['Status', 'Count']
    fig = px.bar(Exited, y='Count', x='Status', title='Exited Customers Distribution', color_discrete_sequence=['blue'])
    st.plotly_chart(fig)
    with st.expander("Insights"):
        st.write("""
            - About 12.7% of customers have exited the bank (Exited = 1).
            - The majority (about 87.3%) have not exited the bank (Exited = 0).
        """)

# Joining Year Line Chart
with col2:
    st.subheader("Joining Year Distribution")
    df['joining_year'] = 2024 - df['Tenure']
    year = df['joining_year'].value_counts().reset_index()
    year.columns = ['Joining Year', 'Count']
    year = year.sort_values(by='Joining Year')
    fig = px.line(year, x='Joining Year', y='Count', title="Joining Year Distribution", color_discrete_sequence=['red'])
    st.plotly_chart(fig)
    with st.expander("Insights"):
        st.write("""
            - The year 2022 saw the highest number of customers, totaling 30.331k.
            - Conversely, 2024 had the lowest number of customers, with only 8431.
            - On average, we attract around 27.500k customers each year.
        """)

# Active Member Distribution Pie Chart
with col3:
    st.subheader("Active Member Distribution")
    fig = px.pie(df, names='IsActiveMember', title="Active Member Distribution", color_discrete_sequence=['red', 'black'])
    st.plotly_chart(fig)
    with st.expander("Insights"):
        st.write("""
            - Approximately 50.3% of customers are active members (IsActiveMember).
        """)
