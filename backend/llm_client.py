import os
import json
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Read Groq API Key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise Exception("GROQ_API_KEY not found in .env file")

# Initialize Groq client
client = Groq(api_key=api_key)



def review_code(
    file_name,
    code,
    context="",
    business_context="",
    sonar_issues=None,
    jira_story=""
):
    print("==============================")
    print("Entering review_code")
    print("File:", file_name)
    print("Jira Story Length:", len(jira_story))
    print("==============================")
    if sonar_issues is None:
        sonar_issues = []

    prompt = f"""
You are a Senior Java Code Reviewer.

Your responsibility is to verify whether the implementation satisfies the business requirement.

====================================================
User Story (Jira)
====================================================

{jira_story}


====================================================
Business Context (Neo4j Knowledge Graph)
====================================================

{business_context}


====================================================
Current Java Code
====================================================

{code}


====================================================
Related Code Context (ChromaDB RAG)
====================================================

{context}


====================================================
SonarQube Findings
====================================================

{json.dumps(sonar_issues, indent=2)}

====================================================
Review Instructions
====================================================

Review the implementation against the Jira requirements.

Check:

- Missing business validations
- Incorrect business rules
- Incorrect data flow
- Security issues
- Performance issues
- Maintainability problems

Use Neo4j context to understand relationships between classes and methods.

Use RAG context only for dependency understanding.

Do not repeat SonarQube findings.

Return ONLY valid JSON.

{{
    "file":"{file_name}",
    "story_validation":{{
        "implemented": true,
        "missing_requirements":[]
    }},
    "summary":"",
    "issues":[
        {{
            "severity":"Critical|High|Medium|Low",
            "category":"Bug|Security|Performance|BestPractice",
            "line":0,
            "description":"",
            "recommendation":""
        }}
    ]
}}"""

    try:
        print("==============================")
        print("Calling Groq")
        print("File:", file_name)
        print("Jira Story Length:", len(jira_story))
        print("Business Context Length:", len(business_context))
        print("==============================")


        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        content = response.choices[0].message.content.strip()

        # Remove markdown if the model returns it
        content = (
            content
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        return json.loads(content)

    except json.JSONDecodeError:

        print("Invalid JSON returned by LLM")
        print(content)

        return {
            "file": file_name,
            "summary": "Unable to parse LLM response.",
            "issues": [
                {
                    "severity": "Low",
                    "category": "LLM",
                    "line": 0,
                    "description": "LLM returned invalid JSON.",
                    "recommendation": "Review the raw response."
                }
            ]
        }

    except Exception as e:

        print("Groq Error:", str(e))

        return {
            "file": file_name,
            "summary": "LLM request failed.",
            "issues": [
                {
                    "severity": "High",
                    "category": "LLM",
                    "line": 0,
                    "description": str(e),
                    "recommendation": "Verify the Groq API key, network connectivity, and model configuration."
                }
            ]
        }