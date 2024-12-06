from pypdf import PdfReader
import os
import re
import requests
def get_data():
    return extract_pdf_data()
    
def download_and_save_pdf(pdf_download_url=None):

    if pdf_download_url is not None:
        current_directory = os.path.dirname(os.path.abspath(__file__))
        parent_directory = os.path.dirname(current_directory)
        directory = os.path.join(parent_directory, "/tmp")

        if not os.path.exists("./tmp"):
            os.makedirs("./tmp")

        file_path = os.path.join("./tmp", "incident_report.pdf")
        
        # Download the PDF
        response = requests.get(pdf_download_url)
        response.raise_for_status()
        
        with open(file_path, 'wb') as f:
            f.write(response.content)
            
def is_date_time(parts):
    time_pattern = r'^\d{1,2}:\d{2}$'
    if len(parts) >= 2 and re.match(time_pattern, parts[1]):
        return True
    return False


def extract_pdf_data(pdf_file_path="./tmp/incident_report.pdf"):
    try:        
        formatted_data = [] 
        reader = PdfReader(pdf_file_path)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            lines = page.extract_text(extraction_mode="layout").split('\n')
            
            for line in lines:
                data_elements = [element.strip() for element in re.split(r"\s{3,}", line.strip())]

                if len(data_elements) > 1 and data_elements[0] and data_elements[0][0].isdigit():
                    data_elements += [''] * (5 - len(data_elements))  
                    formatted_data.append(tuple(data_elements))
        return formatted_data
    except Exception as e:
        print("Exception-->",e)