from pydantic import BaseModel
from typing import List, Optional

class JiraIssue(BaseModel):
    id: str
    summary: str
    status: str
    priority: Optional[str] = None
    created: str
    updated: str

class TestResult(BaseModel):
    test_case_id: str
    status: str
    execution_time: float
    error_message: Optional[str] = None

class AutomationHealthReport(BaseModel):
    total_tests: int
    passed_tests: int
    failed_tests: int
    issues: List[JiraIssue]
    test_results: List[TestResult]