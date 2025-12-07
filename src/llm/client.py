"""Run this model in Python

> pip install azure-ai-inference
"""
import os
import json
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import AssistantMessage, SystemMessage, UserMessage, TextContentItem
from azure.core.credentials import AzureKeyCredential

def analyze_trends(jira_data, test_results):
    client = ChatCompletionsClient(
        endpoint="https://models.inference.ai.azure.com",
        credential=AzureKeyCredential(os.environ["GITHUB_TOKEN"]),
        api_version="2024-08-01-preview",
    )

    # Prepare your data as text
    jira_text = str(jira_data)
    test_text = str(test_results)

    user_prompt = f"Test Results: {test_text}\nAre tests improving over time?"

    response = client.complete(
        messages = [
            SystemMessage(content = (
                "You are a test automation health assistant. "
                "Analyze the following JIRA issues. "
                "Identify trends, correlations, and summarize the health bug life cycle for this JIRA project.\n\n"
                f"JIRA Data:\n{jira_data}\n\nTest Results:\n{test_results}"
            )),
            # UserMessage(content = [
            #     TextContentItem(text = "What trends and correlations do you see in the provided data?"),
            # ]),
                        UserMessage(content = [
                TextContentItem(text = "Give a detailed statistical analysis of the trends in the test results and JIRA issues. "),
            ]),
        ],
        model="gpt-4.1-nano",
        tools=[],
        response_format="text",
        temperature=1,
        top_p=1,
    )

    return response.choices[0].message.content

class LLMModel:
    # ...existing code...

    def predict_health(self, jira_data, automated_test_results):

        # Serialize data as JSON for better LLM understanding
        jira_json = json.dumps(jira_data, default=str, indent=2)
        test_results_json = json.dumps(automated_test_results, default=str, indent=2)

        print("JIRA JSON serialization:\n", jira_json)
        print("Test Results JSON serialization:\n", test_results_json)

        trends = analyze_trends(jira_json, test_results_json)
        return {
            "trends_analysis": trends,
            "total_issues": len(jira_data) if jira_data is not None else 0,
            "total_tests": len(automated_test_results) if automated_test_results is not None else 0,
        }

