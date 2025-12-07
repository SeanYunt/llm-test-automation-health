import os
import pandas as pd

class CSVParser:
    def parse_csv(self, file_path):
        print(os.path.curdir)  # Should print cwd
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV file not found: {file_path}")
        try:
            data = pd.read_csv(file_path)
            return data
        except Exception as e:
            raise ValueError(f"Error parsing CSV file '{file_path}': {e}")

    def validate_data(self, data):
        required_columns = ['test_case', 'result', 'timestamp']
        for column in required_columns:
            if column not in data.columns:
                raise ValueError(f"Missing required column: {column}")
        return True