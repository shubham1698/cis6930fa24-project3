# cis6930-project3

Name: Shubham Manoj Singh

# Assignment Description 

In Project 3 we are tasked with creating an interactive web interface to visualize data collected from Norman Police Department incident reports. The interface should accept NormanPD-style incident PDFs via file upload or URL and provide three visualizations: clustering of records, a bar graph comparing results  and a third visualization of our choice. Additionally, the interface must display key statistics over the collected data and include a method for user feedback. As part of the deliverables, create a narrated video demo showcasing all functionality, host it on a cloud platform like YouTube, and include the video link in the README file. This project focuses on presenting data effectively to end users, representing the final stage in the data pipeline.

# How to install

To install the necessary packages for this project, navigate to the root of the project directory and run : pipenv install -e .

## How to run

1) pipenv run streamlit run main.py

[C:\Users\shubh\Documents\UFProject\DE\cis6930-project0\de_rec_proj_0.mp4](https://github.com/user-attachments/assets/2518c324-3648-41ba-a7c5-5da9d41a31b1)

### main.py

### `preprocess_data(data)`
- Converts raw data into a structured DataFrame.
- Ensures `Date` is in datetime format.
- Returns the cleaned DataFrame.

### `visualize_clusters(df)`
- Combines `Nature` and `Location` for text-based clustering.
- Uses **TF-IDF** for vectorization and **KMeans** for clustering.
- Reduces dimensions with **PCA** for a 2D scatter plot.
- Outputs a Plotly scatter plot of incident clusters.

### `incident_type_bar_chart(df)`
- Counts the frequency of each incident type (`Nature`).
- Creates a bar chart showing the distribution of incident types.

### `most_frequent_detail_pie_chart(df)`:
- Counts the occurrences of each `Nature`.
- Highlights the most frequent type in the pie chart title.
- Outputs a pie chart showing proportions of incident types.

### `main()`:
- Handles data input (PDF upload or URL).
- Processes and displays raw data.
- Generates and displays three visualizations:
  1. Clusters of incidents.
  2. Incident type distribution.
  3. Most frequent incident type.


### data_cleaning_extractions.py

These functions work together to download a PDF incident report, extract relevant information from it, and structure the data for further use or analysis.

### `get_data()`:
   Returns extracted text data from a PDF file by calling `extract_text_from_pdf()`.

### `download_and_save_pdf(pdf_download_path=None)`:
   Downloads a PDF file from a given URL and saves it to a local directory.

### `is_date_time(parts)`:
   Checks if a given list of string parts contains a time in the format HH:MM.

### `extract_text_from_pdf()`:
   Extracts structured data from a PDF file containing incident reports. It processes each line, identifying and organizing information such as time, incident number, location, nature of incident, and ORI. The function handles multi-line entries and special cases, returning a list of structured data entries.

#### test_data_cleaning_extactions.py

#### `test_is_date_time`

Test the is_date_time function.This test checks the is_date_time function's ability to correctly identify valid and invalid date-time inputs. It verifies the behavior for both valid and invalid inputs and asserts that the function behaves as expected.

### **test_visualization**

1. `setUp(self)`
   - **Purpose**: Prepares sample data for testing.
   - **Input**: None.
   - **Output**: A sample DataFrame (`self.data`).
   - **Description**: Sets up consistent test data for all test cases.

2. `test_visualize_clusters(self)`
   - **Purpose**: Tests the `visualize_clusters` function.
   - **Input**: Sample DataFrame.
   - **Output**: Asserts output is a Plotly `Figure`.
   - **Description**: Ensures `visualize_clusters` generates a valid scatter plot.

3. `test_incident_type_bar_chart(self)`
   - **Purpose**: Tests the `incident_type_bar_chart` function.
   - **Input**: Sample DataFrame.
   - **Output**: Asserts output is a Plotly `Figure`.
   - **Description**: Confirms the bar chart function works correctly.

4. `test_most_frequent_detail_pie_chart(self)`
   - **Purpose**: Tests the `most_frequent_detail_pie_chart` function.
   - **Input**: Sample DataFrame.
   - **Output**: Asserts output is a Plotly `Figure`.
   - **Description**: Verifies pie chart functionality and highlights the most frequent detail.

## Bugs and Assumptions

- I have made an assumed that the location string will properly spaced as i am using whitespaces count to parse data.
- The link sent as in Input will be an valid string.
