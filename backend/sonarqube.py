import requests
import os

SONAR_URL = "http://localhost:9000"
SONAR_PROJECT = "ai-code-review"
SONAR_TOKEN = os.getenv("SONAR_TOKEN")


def get_sonar_issues(file_path):
    """
    Returns SonarQube issues for a specific Java file.
    """

    url = f"{SONAR_URL}/api/issues/search"

    params = {
        "componentKeys": SONAR_PROJECT,
        "ps": 500
    }

    response = requests.get(
        url,
        params=params,
        auth=(SONAR_TOKEN, "")
    )

    if response.status_code != 200:
        print("Unable to fetch SonarQube issues")
        return []

    data = response.json()

    issues = []

    for issue in data.get("issues", []):

        component = issue.get("component", "")

        if file_path in component:

            issues.append({

                "severity": issue["severity"],

                "line": issue.get("line", 0),

                "rule": issue["rule"],

                "message": issue["message"]

            })

    return issues