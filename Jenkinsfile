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


                        echo "First Jenkins build detected"


                        git diff HEAD~1 HEAD --name-only \
                        | grep "\\.java$" \
                        > changed_files.txt || true


                    else


                        git diff $GIT_PREVIOUS_COMMIT $GIT_COMMIT --name-only \
                        | grep "\\.java$" \
                        > changed_files.txt || true


                    fi



                    echo "--- Changed Java Files for AI Review ---"

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

                    echo "Sending review packet to AI Review Agent..."



                    curl \

                    -X POST \

                    -F "file=@review.tar.gz" \

                    "$REVIEW_API" \

                    -o ai-review-result.json



                    echo "--- AI Review Result ---"

                    cat ai-review-result.json



                '''

            }

        }





        stage('Generate HTML Report') {


            steps {


                sh '''

                    python3 scripts/generate_report.py


                    echo "HTML Report Generated"


                '''

            }

        }





        stage('AI Quality Gate') {


            steps {


                script {


                    def review = readJSON file:'ai-review-result.json'



                    def criticalIssues = 0



                    review.reviews.each { file ->


                        file.chunk_reviews.each { chunk ->



                            chunk.review.issues.each { issue ->



                                if(issue.severity == "Critical") {


                                    criticalIssues++


                                }


                            }


                        }


                    }



                    echo "Critical Issues Found: ${criticalIssues}"



                    if(criticalIssues > 0) {


                        currentBuild.result = "FAILURE"


                        error(

                        "AI Review Failed: ${criticalIssues} Critical issues found"

                        )


                    }


                }


            }


        }





        stage('GitHub Status Check') {


            steps {


                script {



                    def status =

                    currentBuild.result == "FAILURE"

                    ? "failure"

                    : "success"





                    withCredentials([


                        string(

                            credentialsId: 'github-token',

                            variable: 'GITHUB_TOKEN'

                        )


                    ]) {



                        sh """


                        curl \

                        -X POST \

                        -H "Authorization: token \$GITHUB_TOKEN" \

                        -H "Accept: application/vnd.github+json" \

                        https://api.github.com/repos/PadmavathiVelmurugan/ai-code-review-poc/statuses/\${GIT_COMMIT} \

                        -d '{


                          "state":"${status}",


                          "description":"AI Code Review completed",


                          "context":"AI Reviewer"


                        }'



                        """


                    }


                }


            }


        }
        stage('Post PR Comment') {

    steps {

        script {

            withCredentials([
                string(
                    credentialsId: 'github-token',
                    variable: 'GITHUB_TOKEN'
                )
            ]) {


                sh '''

                echo "Posting AI Review comment to GitHub PR..."


                curl \
                -X POST \
                -H "Authorization: token $GITHUB_TOKEN" \
                -H "Accept: application/vnd.github+json" \
                https://api.github.com/repos/PadmavathiVelmurugan/ai-code-review-poc/issues/${CHANGE_ID}/comments \
                -d @comment.json


                '''

            }

        }

    }

}
stage('Generate PR Comment') {

    steps {

        script {

            def review = readJSON file: 'ai-review-result.json'

            def body = "## 🤖 AI Code Review Result\n\n"

            body += "✅ Review Completed\n\n"

            review.reviews.each { file ->

                body += "### File: ${file.file}\n\n"

                file.chunk_reviews.each { chunk ->

                    body += "**Method:** ${chunk.method}\n\n"

                    chunk.review.issues.each { issue ->

                        body += "- **${issue.severity}**: ${issue.description}\n"

                    }

                    body += "\n"
                }

            }

            writeJSON(
                file: 'comment.json',
                json: [body: body],
                pretty: 4
            )

            echo "Generated comment.json"

        }

    }

}



    }



    post {



        always {



            echo "AI Review Pipeline Completed"



        }



    }


}