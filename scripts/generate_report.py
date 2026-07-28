
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

        for issue in chunk["review"]["issues"]:

            html += f"""

            <p>
            <b>
            Severity:
            </b>
            {issue['severity']}

            <br>

            <b>
            Description:
            </b>

            {issue['description']}

            <br>

            <b>
            Recommendation:
            </b>

            {issue['recommendation']}

            </p>

            <hr>

            """


html+="</body></html>"


open(
"ai-review-report.html",
"w"
).write(html)