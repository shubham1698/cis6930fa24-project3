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

# Assuming you have a module for PDF extraction
from DataProcessing.data_cleaning_extractions import download_and_save_pdf, extract_pdf_data

def preprocess_data(data):
    df = pd.DataFrame(data, columns=["Date", "Incident Number", "Location", "Nature", "Incident ORI"])
    
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    
    return df

def visualize_clusters(df):
    df['combined_text'] = df['Nature'] + ' ' + df['Location']
    
    vectorizer = TfidfVectorizer(stop_words='english')
    text_vectors = vectorizer.fit_transform(df['combined_text'].fillna(''))
    
    kmeans = KMeans(n_clusters=5, random_state=42)
    clusters = kmeans.fit_predict(text_vectors)
    
    pca = PCA(n_components=2)
    reduced_vectors = pca.fit_transform(text_vectors.toarray())
    
    cluster_df = pd.DataFrame({
        'PCA1': reduced_vectors[:, 0],
        'PCA2': reduced_vectors[:, 1],
        'Cluster': clusters,
        'Nature': df['Nature'],
        'Location': df['Location'],
        'Date': df['Date']
    })
    
    fig = px.scatter(
        cluster_df, 
        x='PCA1', 
        y='PCA2', 
        color='Cluster', 
        hover_data=['Nature', 'Location', 'Date'],
        title='Incident Clusters',
        labels={'Cluster': 'Cluster Group'}
    )
    
    return fig

def incident_type_bar_chart(df):
    incident_counts = df['Nature'].value_counts()
    
    fig = px.bar(
        x=incident_counts.index, 
        y=incident_counts.values,
        title='Incident Types',
        labels={'x': 'Nature of Incident', 'y': 'Number of Incidents'}
    )
    
    return fig

def most_frequent_detail_pie_chart(df):
    try:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

        df = df.dropna(subset=['Nature'])

        detail_counts = df['Nature'].value_counts().reset_index()
        detail_counts.columns = ['Nature', 'Count']

        most_frequent_detail = detail_counts.iloc[0]

        title = f"Most Frequent Detail: {most_frequent_detail['Nature']} ({most_frequent_detail['Count']} incidents)"

        fig = px.pie(
            detail_counts,
            names='Nature',
            values='Count',
            title=title,
            labels={'Nature': 'Nature', 'Count': 'Number of Incidents'}
        )

        return fig
    except Exception as e:
        st.error(f"An error occurred while generating the pie chart: {e}")
    
def main():
    st.title("Norman Police Incident Data Visualization")
    
    st.sidebar.header("Data Input")
    uploaded_file = st.sidebar.file_uploader("Upload PDF", type=['pdf'])
    incident_url = st.sidebar.text_input("Or enter PDF URL")

        # CSS for animation
    st.markdown(
        """
        <style>
        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(-20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
            
        .animated-heading {
            font-size: 1.25em;
            color: #fffff;
            text-align: center;
            animation: fadeIn 2s ease-in-out;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

        # Animated heading
    st.markdown('<div class="animated-heading">Uncover Trends, Explore Insights, and Analyze Incidents Seamlessly</div>', unsafe_allow_html=True)
    
    
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
        
        df = preprocess_data(data)


        st.subheader("Extracted Incident Data")
        st.dataframe(df)
        
        st.header("Data Visualizations")
        
        st.subheader("1. Incident Clusters")
        cluster_fig = visualize_clusters(df)
        st.plotly_chart(cluster_fig)
        
        st.subheader("2. Incident Type Distribution")
        bar_fig = incident_type_bar_chart(df)
        st.plotly_chart(bar_fig)
        
        st.subheader("3. Incident Distribution Over Time")
        pie_fig = most_frequent_detail_pie_chart(df)
        st.plotly_chart(pie_fig)

if __name__ == "__main__":
    main()