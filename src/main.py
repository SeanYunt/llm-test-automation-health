import configparser
import os
from llm.model import LLMModel
from jira_client.fetcher import JiraFetcher
from csv_parser.parser import CSVParser
from utils.helpers import log_message, format_results
from jira import JIRA
from pydantic import BaseModel

class Config(BaseModel):
    api_token: str
    email: str
    jira_url: str
    jira_project_key: str
    csv_file_path: str

def read_pyvenv_cfg():
    cfg_path = os.path.join(os.path.dirname(os.__file__), '..', 'pyvenv.cfg')  # adjusts as needed or provide absolute path
    if not os.path.exists(cfg_path):
        cfg_path = 'pyvenv.cfg'  # fallback if script runs from venv root
    config = configparser.ConfigParser()
    # configparser requires a section header, so fake one if not present
    with open(cfg_path, 'r') as f:
        content = f.read()
    if not content.startswith("[DEFAULT]"):
        content = "[DEFAULT]\n" + content
    config.read_string(content)
    cfg = config['DEFAULT']
    return {
        "api_token": cfg.get('api_token'),
        "email": cfg.get('email'),
        "jira_url": cfg.get('jira_url'),
        "jira_project_key": cfg.get('jira_project_key'),
        "csv_file_path": cfg.get('csv_file_path')
    }

def main():
    log_message("Initializing the LLM...")
    llm_model = LLMModel()
    llm_model.load_model()

    log_message("Fetching data from Jira...")
    pyvenv_config = read_pyvenv_cfg()
    config = Config(
        api_token=pyvenv_config['api_token'],
        email=pyvenv_config['email'],
        jira_url=pyvenv_config['jira_url'],
        jira_project_key=pyvenv_config['jira_project_key'],
        csv_file_path=pyvenv_config['csv_file_path']
    )

    jira_client = JIRA(server=config.jira_url, basic_auth=(config.email, config.api_token))

    jira_fetcher = JiraFetcher(jira_client)
    issues = jira_fetcher.fetch_issues(config.jira_project_key)

    log_message("Parsing CSV results...")
    csv_parser = CSVParser()
    parsed_results = csv_parser.parse_csv(config.csv_file_path)

    # Convert parsed_results (likely a DataFrame) to a list of dicts with expected keys
    if hasattr(parsed_results, "to_dict"):
        parsed_results_dict = []
        for idx, row in parsed_results.iterrows():
            # Extract status from group column
            group = row.get("group", "")
            if "@test.status:fail" in group:
                status = "fail"
            elif "@test.status:pass" in group:
                status = "pass"
            else:
                status = "unknown"
            parsed_results_dict.append({
                "test_case_id": str(idx),
                "status": status,
                "execution_time": row.get("time"),
                "value": row.get("value"),
            })
    else:
        parsed_results_dict = parsed_results

    log_message("Evaluating test automation health...")
    try:
        health_status = llm_model.predict_health(issues, parsed_results_dict)
    except Exception as e:
        log_message(f"Error in predict_health: {e}")
        raise

    if health_status is None:
        log_message("No health status returned from LLM model.")
        return

    log_message("Formatting results...")
    formatted_results = format_results(health_status)

    log_message("Test automation health evaluation completed.")
    print(formatted_results)

if __name__ == "__main__":
    main()