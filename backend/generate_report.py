
import json


data=json.load(
    open("ai-review-result.json")
)


html="""

<html>
<head>
<title>
AI Code Review Report
</title>
</head>

<body>

<h1>
AI Code Review Report
</h1>

"""


for review in data["reviews"]:

    html += f"""
    <h2>{review['file']}</h2>
    """

    for chunk in review["chunk_reviews"]:

     html += f"""
     <h3>
     Method: {chunk['method']}
     </h3>
     """

     # Add the summary here
     summary = chunk["review"].get("summary", "")

     if summary:
        html += f"""
        <p>
        <b>Summary:</b> {summary}
        </p>
        """

     # Get issues
     issues = chunk["review"].get("issues", [])

     if not issues:
        html += """
        <p style="color:green;">
        <b>✅ No issues found. No recommendations.</b>
        </p>
        <hr>
        """
     else:
        for issue in issues:

            html += f"""

            <p>

            <b>Severity:</b>
            {issue['severity']}

            <br>

            <b>Category:</b>
            {issue.get('category', '-')}

            <br>

            <b>Description:</b>
            {issue['description']}

            <br>

            <b>Recommendation:</b>
            {issue['recommendation']}

            </p>

            <hr>

            """

html+="</body></html>"


open(
"ai-review-report.html",
"w"
).write(html)