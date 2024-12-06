import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objs as go
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Assuming you have a module for PDF extraction
from DataProcessing.data_cleaning_extractions import download_and_save_pdf, extract_pdf_data

def preprocess_data(data):
    """
    Preprocess the extracted data into a DataFrame
    """
    # Ensure data is converted to DataFrame with consistent columns
    df = pd.DataFrame(data, columns=["Date", "Incident Type", "Location", "Details", "Extra Column"])
    
    # Convert date to datetime
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    
    return df

def visualize_clusters(df):
    """
    Create a clustering visualization using TF-IDF and PCA
    """
    # Combine text features
    df['combined_text'] = df['Incident Type'] + ' ' + df['Location']
    
    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(stop_words='english')
    text_vectors = vectorizer.fit_transform(df['combined_text'].fillna(''))
    
    # Clustering
    kmeans = KMeans(n_clusters=5, random_state=42)
    clusters = kmeans.fit_predict(text_vectors)
    
    # Dimensionality Reduction
    pca = PCA(n_components=2)
    reduced_vectors = pca.fit_transform(text_vectors.toarray())
    
    # Create DataFrame for plotting
    cluster_df = pd.DataFrame({
        'PCA1': reduced_vectors[:, 0],
        'PCA2': reduced_vectors[:, 1],
        'Cluster': clusters,
        'Incident Type': df['Incident Type'],
        'Location': df['Location'],
        'Date': df['Date']
    })
    
    # Interactive Plotly Scatter Plot
    fig = px.scatter(
        cluster_df, 
        x='PCA1', 
        y='PCA2', 
        color='Cluster', 
        hover_data=['Incident Type', 'Location', 'Date'],
        title='Incident Clusters',
        labels={'Cluster': 'Cluster Group'}
    )
    
    return fig

def incident_type_bar_chart(df):
    """
    Create a bar chart of incident types
    """
    # Count incidents by type
    incident_counts = df['Details'].value_counts()
    
    # Create bar chart
    fig = px.bar(
        x=incident_counts.index, 
        y=incident_counts.values,
        title='Incident Types',
        labels={'x': 'Details', 'y': 'Number of Incidents'}
    )
    
    return fig

def most_frequent_detail_pie_chart(df):
    """
    Create a pie chart showing the distribution of details and highlighting the most frequent one.
    """
    try:
        # Ensure the Date column is in datetime format
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

        # Drop rows with missing or invalid 'Details'
        df = df.dropna(subset=['Details'])

        # Group by 'Details' and count occurrences
        detail_counts = df['Details'].value_counts().reset_index()
        detail_counts.columns = ['Detail', 'Count']

        # Find the most frequent detail
        most_frequent_detail = detail_counts.iloc[0]

        # Highlight the most frequent detail in the title
        title = f"Most Frequent Detail: {most_frequent_detail['Detail']} ({most_frequent_detail['Count']} incidents)"

        # Create a pie chart
        fig = px.pie(
            detail_counts,
            names='Detail',
            values='Count',
            title=title,
            labels={'Detail': 'Detail', 'Count': 'Number of Incidents'}
        )

        return fig
    except Exception as e:
        st.error(f"An error occurred while generating the pie chart: {e}")
    
def main():
    st.title("Norman Police Incident Data Visualization")
    
    # Sidebar for file upload
    st.sidebar.header("Data Input")
    uploaded_file = st.sidebar.file_uploader("Upload PDF", type=['pdf'])
    incident_url = st.sidebar.text_input("Or enter PDF URL")
    
    # Process button
    if st.sidebar.button("Process Data"):
        # Data extraction
        if uploaded_file:
            st.write("Processing uploaded file...")
            data = extract_pdf_data(uploaded_file)
        elif incident_url:
            st.write("Processing URL...")
            download_and_save_pdf(incident_url)
            data = extract_pdf_data("./tmp/incident_report.pdf")
        else:
            st.error("Please upload a file or provide a URL")
            return
        
        # Preprocess data
        df = preprocess_data(data)
        
        # Display raw data
        st.subheader("Extracted Incident Data")
        st.dataframe(df)
        
        # Visualization Section
        st.header("Data Visualizations")
        
        # Clustering Visualization
        st.subheader("1. Incident Clusters")
        cluster_fig = visualize_clusters(df)
        st.plotly_chart(cluster_fig)
        
        # Bar Chart of Incident Types
        st.subheader("2. Incident Type Distribution")
        bar_fig = incident_type_bar_chart(df)
        st.plotly_chart(bar_fig)
        
        # Temporal Heatmap
        st.subheader("3. Incident Distribution Over Time")
        temporal_fig = most_frequent_detail_pie_chart(df)
        st.plotly_chart(temporal_fig)

if __name__ == "__main__":
    main()