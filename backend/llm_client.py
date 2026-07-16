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


def review_code(file_name, code, context="", sonar_issues=None):

    if sonar_issues is None:
        sonar_issues = []

    prompt = f"""
You are a Senior Java Code Reviewer.

Review ONLY the provided Java code.

Use the following information.

====================================================
Project Context (RAG)
====================================================

{context}

====================================================
SonarQube Findings
====================================================

{json.dumps(sonar_issues, indent=2)}

====================================================
Current Java Code
====================================================

{code}

====================================================
Instructions
====================================================

1. Review ONLY this Java code.
2. Use the RAG context only to understand dependencies.
3. Treat SonarQube findings as existing static-analysis results.
4. Do NOT repeat SonarQube findings.
5. Only report:
   - Business logic bugs
   - Security issues missed by SonarQube
   - Performance improvements
   - Maintainability issues
   - Best practices
6. If there are no issues, return an empty issues array.
7. Return ONLY valid JSON.
8. Do NOT use markdown or code fences.

Return JSON exactly in this format:

{{
    "file":"{file_name}",
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
}}
"""

    try:

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