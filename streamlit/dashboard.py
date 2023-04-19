import pandas as pd 
import streamlit as st 
import seaborn as sns 
import matplotlib.pyplot as plt 
import plotly.express as px 
import plotly.graph_objects as go 
from google.cloud import bigquery 
import os

# Authenticate with Google Cloud 
creds_path = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
client = bigquery.Client.from_service_account_json(creds_path)

# Define a function to load data from BigQuery 
@st.cache_data 
def load_data(): 
    query = """ 
        SELECT severity,severity_description,state,city,weather_condition
        FROM `de-project-franklyne.production.fact_accidents` 
    """ 
    results = client.query(query).to_dataframe() 
    return results

# Load the US Accidents dataset into a DataFrame 
accidents = load_data() 

# Set app title
st.title("US Accidents Analysis")

# Display total count of accidents
# st.write(f"Total number of accidents: {accidents.shape[0]}")

# Sidebar options 
analysis_type = st.sidebar.selectbox("Select Analysis Type", ("Accidents by State", "Accidents by City", "Accident Severity by Weather Condition", "Accident Severity Distribution")) 

# Accidents by State 
if analysis_type == "Accidents by State": 
    st.header("US Accidents by State") 
    state_counts = accidents['state'].value_counts()[:20]
    fig = px.bar(x=state_counts.index, y=state_counts.values)
    
    # Add X and Y axis labels
    fig.update_xaxes(title_text="State")
    fig.update_yaxes(title_text="Number of Accidents")
    
    st.plotly_chart(fig)

# Accidents by City
elif analysis_type == "Accidents by City":
    st.header("US Accidents by City")
    city_counts = accidents['city'].value_counts().sort_values(ascending=False)[:20]
    fig, ax = plt.subplots()
    sns.barplot(x=city_counts.index, y=city_counts.values, ax=ax)

    # Add X and Y axis labels
    ax.set_xlabel("City")
    ax.set_ylabel("Number of Accidents")

    # Add plot title
    ax.set_title("Number of Accidents by City")

    plt.xticks(rotation=90)
    
    # Set figure size to fit Streamlit app
    fig.set_size_inches(12, 8)
    
    st.pyplot(fig)

# Accident Severity by Weather Condition 
elif analysis_type == "Accident Severity by Weather Condition": 
    st.header("Accident Severity by Weather Condition") 
    weather_severity = accidents.groupby('weather_condition')['severity'].mean().sort_values(ascending=False) 
    fig = px.bar(x=weather_severity.index, y=weather_severity.values) 
    
    # Add X and Y axis labels
    fig.update_xaxes(title_text="Weather Condition")
    fig.update_yaxes(title_text="Severity")
    
    st.plotly_chart(fig) 

# Accident Severity Distribution 
elif analysis_type == "Accident Severity Distribution":
    st.header("Accident Severity Distribution")
    severity_counts = accidents['severity_description'].value_counts()
    values = severity_counts.values.tolist()
    labels = severity_counts.index.tolist()
    colors = px.colors.qualitative.Pastel
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_traces(marker=dict(colors=colors))
    fig.update_layout(title="Percentage of Accidents by Severity Level")
    st.plotly_chart(fig)