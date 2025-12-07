class JiraFetcher:
    def __init__(self, jira_client):
        self.jira_client = jira_client

    def fetch_issues(self, project_key):
        jql_query = f'project = {project_key} and issuetype = "Bug" and status != "Done"'
        issues = self.jira_client.search_issues(jql_query)
        return issues

    def fetch_test_results(self, issue_key):
        issue = self.jira_client.issue(issue_key)
        test_results = issue.fields.customfield_test_results  # Adjust based on actual field name
        return test_results

# Example of how to initialize jira_client:
# Example API token (do not hardcode secrets in production):
