# LLM Test Automation Health

## Overview
This project aims to determine the health of test automation by leveraging data from Jira and raw test results in CSV format. It utilizes a language model to analyze the data and provide insights into the effectiveness of the test automation processes.

## Project Structure
```
llm-test-automation-health
├── src
│   ├── main.py          # Entry point of the application
│   ├── llm
│   │   └── model.py     # Contains the LLMModel class for predictions
│   ├── jira_client
│   │   └── fetcher.py   # JiraFetcher class for fetching data from Jira
│   ├── csv_parser
│   │   └── parser.py     # CSVParser class for parsing CSV files
│   ├── utils
│   │   └── helpers.py    # Utility functions for logging and formatting
│   └── custom_types
│       └── schemas.py    # Data schemas for validation
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Setup Instructions
1. Clone the repository:
   ```
   git clone <repository-url>
   cd llm-test-automation-health
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
To run the application, execute the following command:
```
python src/main.py
```

## Functionality
- **Data Fetching**: Connects to the Jira API to retrieve relevant test automation data.
- **CSV Parsing**: Reads and processes raw test results from CSV files.
- **Health Prediction**: Utilizes a language model to analyze the data and predict the health of the test automation efforts.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
