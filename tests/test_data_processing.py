import unittest
import os
from fpdf import FPDF
import sys
from unittest.mock import patch, MagicMock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from DataProcessing.data_cleaning_extractions import download_and_save_pdf, get_data, is_date_time, extract_pdf_data
def create_test_pdf(file_path):
    pdf = FPDF()
    pdf.add_page()

    # Add sample content similar to your expected data
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="8/1/2024 20:13           2024-00055650           3400 N I35 SB I         Traffic Stop        OK0140200", ln=True)
    pdf.cell(200, 10, txt="8/1/2024 20:16           2024-00055651           1507 W LINDSEY ST       Follow Up           OK0140200", ln=True)
    
    pdf.output(file_path)

class TestPDFExtraction(unittest.TestCase):

        


    def setUp(self):
        """Create tmp directory if it does not exist."""
        tmp_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tmp")
        self.test_pdf_path = "./tmp/test_incident_report.pdf"
        create_test_pdf(self.test_pdf_path)
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)

    def tearDown(self):
        """Clean up by removing the test PDF after each test."""
        expected_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tmp", "incident_report.pdf")
        if os.path.exists(expected_path):
            os.remove(expected_path)
    
    def test_is_date_time(self):
        valid_input = ["12", "12:00", "INCIDENT001"]
        invalid_input = ["12", "InvalidTime", "INCIDENT001"]

        self.assertTrue(is_date_time(valid_input))
        self.assertFalse(is_date_time(invalid_input))
    
    def test_extract_pdf_data(self):
        test_pdf_path = "./tmp/test_incident_report.pdf"

        result = extract_pdf_data(test_pdf_path)
        expected_output = [
            ('8/1/2024 20:13', '2024-00055650', '3400 N I35 SB I', 'Traffic Stop', 'OK0140200'),
            ('8/1/2024 20:16', '2024-00055651', '1507 W LINDSEY ST', 'Follow Up', 'OK0140200')
        ]

        # Check if the result matches the expected output
        self.assertEqual(result, expected_output)
        

    
if __name__ == '__main__':
    unittest.main()
