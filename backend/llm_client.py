import os
import json
from dotenv import load_dotenv
from groq import Groq
import re


# Load environment variables
load_dotenv()


# Read Groq API Key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise Exception("GROQ_API_KEY not found in .env file")


# Initialize Groq client
client = Groq(api_key=api_key)



# ====================================================
# AI Review Rules
# ====================================================

REVIEW_RULES = """

You are reviewing enterprise Java code.

Follow these rules strictly.

====================================================
Method Responsibility Rules
====================================================

1. Review only the responsibility of the provided method.

2. Identify the method purpose from:
   - method name
   - parameters
   - return type
   - called services
   - repository operations


3. Business validations should be reviewed only when the method:
   
   - creates data
   - updates data
   - modifies database state
   - processes transactions


4. Read-only methods should NOT be flagged for missing:
   
   - create validations
   - update validations
   - database write rules
5. Do not report missing functionality if another class/service owns that responsibility.
6. Use Business Context only when a relationship exists.

Example:

If Neo4j shows:

ProductController
       |
       calls
       |
ProductValidator


Do not report missing validation inside ProductController.

Assume validation responsibility belongs to ProductValidator.

Only report an issue if no responsible class exists.


Examples:

A method containing:

repository.save()
repository.update()
entity.setXXX()

can be responsible for:
- validation
- business rules
- data integrity


A method containing:

repository.find()
repository.findAll()
repository.get()

is usually responsible for:
- retrieval correctness
- null handling
- response handling
- performance


A method containing:

repository.delete()

may require existence checks, authorization, or deletion rules only if they are explicitly required by:

- the Jira acceptance criteria
- the business context
- the application architecture

Do not assume these requirements automatically.


====================================================
Jira Validation Rules
====================================================

5. Validate Jira acceptance criteria against only the relevant code.

6. Do not report a missing requirement if another layer is responsible.

Example:

Controller calls:

productService.save(product)

and validation exists in:

ProductService.validatePrice()

Do not report missing validation in Controller.


====================================================
Issue Rules
====================================================

7. Never invent issues.

8. Never force every Jira requirement into every method.

9. Avoid duplicate issues.

10. Report only:

- Business correctness issues
- Security issues
- Performance issues
- Important maintainability issues
====================================================
Requirement Validation Rules
====================================================

11. Validate only the requirements explicitly present in:

- Jira Story
- Business Context
- Current Method

12. Never infer new business requirements.

13. If a requirement is not mentioned in the Jira story or business context,
do not report it as missing.

14. If the Jira story is unrelated to the current method,
mark:

"implemented": true

and

"missing_requirements": []

Do not invent issues.

====================================================
Review Decision Process
====================================================

Before reporting any issue, evaluate the following:

1. Is this method responsible for the Jira requirement?
2. Is the issue visible in the supplied method?
3. Does the Business Context indicate another class owns this responsibility?
4. Is the issue already covered by SonarQube?
5. Is the issue explicitly required by the Jira Story?

Only report an issue if all applicable answers support reporting it.

Otherwise, do not report the issue.

"""



def review_code(
    file_name,
    code,
    method_name="",
    context="",
    business_context="",
    sonar_issues=None,
    jira_story=""
):

    print("==============================")
    print("Entering review_code")
    print("File:", file_name)
    print("Method:", method_name)
    print("Jira Story Length:", len(jira_story))
    print("==============================")


    if sonar_issues is None:
        sonar_issues = []



    prompt = f"""

You are a Senior Java Code Reviewer.

Your responsibility is to verify whether the implementation satisfies the business requirement.


====================================================
Review Rules
====================================================

{REVIEW_RULES}



====================================================
User Story (Jira)
====================================================

{jira_story}



====================================================
Business Context (Neo4j Knowledge Graph)
====================================================

{business_context}



====================================================
Current File
====================================================

{file_name}



====================================================
Current Method
====================================================

{method_name}



====================================================
Current Java Code
====================================================

{code}

====================================================
IMPORTANT RAG INSTRUCTIONS
====================================================

The Related Code Context contains real implementation
retrieved from the project.

Before reporting any missing functionality:

1. Examine the Related Code Context.

2. If another class or service already performs
validation, business rules, discount calculation,
audit logging, notification, authorization,
or persistence,

DO NOT report that functionality as missing in
the current method.

Assume the retrieved code is the correct implementation.

Report a missing requirement ONLY if:

- it is absent from both the current method
- and the retrieved related code.

The retrieved context has higher priority than
assumptions.

====================================================
Related Code Context (ChromaDB RAG)
====================================================

{context}



====================================================
SonarQube Findings
====================================================

{json.dumps(sonar_issues, indent=2)}



====================================================
Review Task
====================================================

Step 1 (Mandatory)

Before reviewing the code, determine whether the supplied method is responsible for implementing any Jira acceptance criterion.

If NO:

- Set

"story_validation": {{

  "implemented": true,
  "missing_requirements": []
}}

- Return issues only if there is a real defect visible in this method.

Do NOT invent missing Jira requirements.
Review priority:

1. Jira acceptance criteria
2. Business correctness
3. SonarQube findings
4. Security
5. Performance
6. Maintainability

Do not generate generic best-practice recommendations unless they indicate an actual defect.

Do not repeat SonarQube findings.

If the supplied method correctly implements its responsibility and satisfies the Jira story, return:

"story_validation": {{
    "implemented": true,
    "missing_requirements": []
}}
and

"issues": []

Do not invent recommendations merely to populate the output.
Return ONLY valid JSON.



Expected JSON format:

{{
    "file":"{file_name}",

    "method":"{method_name}",

    "story_validation":{{

        "implemented": true,

        "missing_requirements":[]

    }},

    "summary":"",

    "issues":[

        {{

            "severity":"Critical|High|Medium|Low",

            "confidence":0.0,

            "category":"Bug|Security|Performance|BestPractice",

            "line":0,

            "description":"",

            "recommendation":""

        }}

    ]

}}

"""


    try:

        print("==============================")
        print("Calling Groq")
        print("File:", file_name)
        print("Method:", method_name)
        print("Business Context Length:", len(business_context))
        print("==============================")


        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[

                {
                    "role":"user",
                    "content":prompt
                }

            ],

            temperature=0,
            response_format={"type": "json_object"}

        )



        content = response.choices[0].message.content.strip()
        print("==============================")
        print("RAW GROQ RESPONSE")
        print(content)
        print("==============================")


        # Remove markdown response
        content = (
            content
            .replace("```json","")
            .replace("```","")
            .strip()
        )
        match = re.search(r'\{.*\}', content, re.DOTALL)

        if not match:
          raise json.JSONDecodeError("No JSON found", content, 0)
        parsed_response = json.loads(content)

        print("==============================")
        print("PARSED RESPONSE TYPE")
        print(type(parsed_response))
        print("==============================")

        return parsed_response



    except json.JSONDecodeError:


        print("Invalid JSON returned by LLM")
        print(content)


        return {

            "file":file_name,

            "method":method_name,

            "summary":"Unable to parse LLM response.",

            "issues":[

                {

                    "severity":"Low",

                    "confidence":0.2,

                    "category":"LLM",

                    "line":0,

                    "description":"LLM returned invalid JSON.",

                    "recommendation":"Review raw LLM response."

                }

            ]

        }



    except Exception as e:


        print("Groq Error:",str(e))


        return {

            "file":file_name,

            "method":method_name,

            "summary":"LLM request failed.",

            "issues":[

                {

                    "severity":"High",

                    "confidence":1.0,

                    "category":"LLM",

                    "line":0,

                    "description":str(e),

                    "recommendation":
                    "Verify Groq API key, network connectivity and model configuration."

                }

            ]

        }