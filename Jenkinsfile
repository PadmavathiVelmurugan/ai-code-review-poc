pipeline {

    agent any

    environment {
        REVIEW_API = "http://host.docker.internal:8000/review"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Git Diff Tracking') {
            steps {
                sh '''
                    echo "Previous Commit: $GIT_PREVIOUS_COMMIT"
                    echo "Current Commit: $GIT_COMMIT"

                    if [ -z "$GIT_PREVIOUS_COMMIT" ]; then
                        echo "First Jenkins build"

                        git diff HEAD~1 HEAD --name-only \
                        | grep "\\.java$" \
                        > changed_files.txt || true
                    else
                        git diff "$GIT_PREVIOUS_COMMIT" "$GIT_COMMIT" --name-only \
                        | grep "\\.java$" \
                        > changed_files.txt || true
                    fi

                    echo "Changed Java Files"
                    cat changed_files.txt
                '''
            }
        }

        stage('Package Review Artifacts') {
            steps {
                sh '''
                    rm -rf review_package review.tar.gz
                    mkdir review_package

                    if [ -d backend/src ]; then
                        cp -r backend/src review_package/
                    fi

                    if [ -f backend/pom.xml ]; then
                        cp backend/pom.xml review_package/
                    fi

                    cp changed_files.txt review_package/

                    tar -czf review.tar.gz -C review_package .
                '''
            }
        }

        stage('AI Code Review Execution') {
            steps {
                sh '''
                    echo "Sending review packet..."

                    curl -X POST \
                      -F "file=@review.tar.gz" \
                      "$REVIEW_API" \
                      -o ai-review-result.json

                    echo "AI Review Result"
                    cat ai-review-result.json
                '''
            }
        }

        stage('Generate HTML Report') {
            steps {
                sh '''
                    python3 backend/generate_report.py
                '''
            }
        }

        stage('Publish HTML Report') {
            steps {
                publishHTML(target: [
                    allowMissing: true,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: '.',
                    reportFiles: 'report.html',
                    reportName: 'AI Code Review Report'
                ])
            }
        }

        stage('AI Quality Gate') {
            steps {
                script {

                    def review = readJSON file: 'ai-review-result.json'

                    int critical = 0

                    review.reviews.each { file ->
                        file.chunk_reviews.each { chunk ->
                            chunk.review.issues.each { issue ->
                                if (issue.severity == "Critical") {
                                    critical++
                                }
                            }
                        }
                    }

                    echo "Critical Issues = ${critical}"

                    if (critical > 0) {
                        error("${critical} Critical issues found")
                    }

                }
            }
        }

        stage('Generate PR Comment') {
            when {
                expression { env.CHANGE_ID }
            }

            steps {
                script {

                    def review = readJSON file: 'ai-review-result.json'

                    def body = "## 🤖 AI Code Review Result\\n\\n"
                    body += "✅ Review Completed\\n\\n"

                    review.reviews.each { file ->

                        body += "### ${file.file}\\n\\n"

                        file.chunk_reviews.each { chunk ->

                            body += "**Method:** ${chunk.method}\\n\\n"

                            chunk.review.issues.each { issue ->
                                body += "- **${issue.severity}** : ${issue.description}\\n"
                            }

                            body += "\\n"
                        }
                    }

                    writeJSON(
                        file: 'comment.json',
                        json: [body: body],
                        pretty: 4
                    )

                }
            }
        }

        stage('Post PR Comment') {

            when {
                expression { env.CHANGE_ID }
            }

            steps {

                withCredentials([
                    string(
                        credentialsId: 'github-pat',
                        variable: 'GITHUB_TOKEN'
                    )
                ]) {

                    sh '''
                    curl -X POST \
                      -H "Authorization: token $GITHUB_TOKEN" \
                      -H "Accept: application/vnd.github+json" \
                      https://api.github.com/repos/PadmavathiVelmurugan/ai-code-review-poc/issues/${CHANGE_ID}/comments \
                      -d @comment.json
                    '''
                }

            }
        }

    }

    post {

        success {

            withCredentials([
                string(
                    credentialsId: 'github-pat',
                    variable: 'GITHUB_TOKEN'
                )
            ]) {

                sh '''
                curl -X POST \
                  -H "Authorization: token $GITHUB_TOKEN" \
                  -H "Accept: application/vnd.github+json" \
                  https://api.github.com/repos/PadmavathiVelmurugan/ai-code-review-poc/statuses/${GIT_COMMIT} \
                  -d '{
                        "state":"success",
                        "description":"AI Code Review Passed",
                        "context":"AI Reviewer"
                      }'
                '''
            }
        }

        failure {

            withCredentials([
                string(
                    credentialsId: 'github-pat',
                    variable: 'GITHUB_TOKEN'
                )
            ]) {

                sh '''
                curl -X POST \
                  -H "Authorization: token $GITHUB_TOKEN" \
                  -H "Accept: application/vnd.github+json" \
                  https://api.github.com/repos/PadmavathiVelmurugan/ai-code-review-poc/statuses/${GIT_COMMIT} \
                  -d '{
                        "state":"failure",
                        "description":"AI Code Review Failed",
                        "context":"AI Reviewer"
                      }'
                '''
            }
        }

        always {
            echo "AI Review Pipeline Completed"
        }
    }
}