import json
import os

INPUT_FILE = "ai-review-result.json"
OUTPUT_FILE = "report.html"

if not os.path.exists(INPUT_FILE):
    print("ai-review-result.json not found")
    exit(1)

with open(INPUT_FILE, "r") as f:
    review = json.load(f)

html = """
<html>
<head>
<title>AI Code Review Report</title>

<style>
body {
    font-family: Arial;
    margin:40px;
}

table {
    width:100%;
    border-collapse:collapse;
}

th,td{
    border:1px solid #ccc;
    padding:10px;
}

th{
    background:#efefef;
}

h1{
    color:#0d47a1;
}
</style>

</head>
<body>

<h1>AI Code Review Report</h1>

"""

html += f"<h3>Status : {review.get('status')}</h3>"
html += f"<h3>Files Reviewed : {review.get('files_reviewed')}</h3>"

for file in review.get("reviews", []):

    html += f"<h2>{file['file']}</h2>"

    html += """
    <table>
    <tr>
        <th>Method</th>
        <th>Severity</th>
        <th>Description</th>
    </tr>
    """

    for chunk in file["chunk_reviews"]:

        method = chunk["method"]

        for issue in chunk["review"]["issues"]:

            html += f"""
            <tr>
                <td>{method}</td>
                <td>{issue['severity']}</td>
                <td>{issue['description']}</td>
            </tr>
            """

    html += "</table><br>"

html += """
</body>
</html>
"""

with open(OUTPUT_FILE, "w") as f:
    f.write(html)

print("HTML report generated successfully.")