import unittest
import os
import sys
import unittest
import pandas as pd
from plotly.graph_objs import Figure
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# Import your visualization functions
from main import (
    visualize_clusters,
    incident_type_bar_chart,
    most_frequent_detail_pie_chart
)

class TestVisualizationFunctions(unittest.TestCase):

    def setUp(self):
        self.data = pd.DataFrame({
            "Date": ["2024-12-01", "2024-12-01", "2024-12-02", "2024-12-03", "2024-12-03"],
            "Incident Number": ["Theft", "Fraud", "Theft", "Assault", "Fraud"],
            "Location": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
            "Nature": ["Stolen goods", "Credit card fraud", "Vehicle theft", "Physical assault", "Online fraud"],
            "Incident ORI": ["Extra1", "Extra2", "Extra3", "Extra4", "Extra5"]
        })

    def test_visualize_clusters(self):
        fig = visualize_clusters(self.data)
        self.assertIsInstance(fig, Figure, "visualize_clusters did not return a Plotly Figure")

    def test_incident_type_bar_chart(self):
        fig = incident_type_bar_chart(self.data)
        self.assertIsInstance(fig, Figure, "incident_type_bar_chart did not return a Plotly Figure")

    def test_most_frequent_detail_pie_chart(self):
        fig = most_frequent_detail_pie_chart(self.data)
        self.assertIsInstance(fig, Figure, "most_frequent_detail_pie_chart did not return a Plotly Figure")

if __name__ == '__main__':
    unittest.main()

