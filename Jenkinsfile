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
                    git diff HEAD~1 HEAD --name-only \
                    | grep "\\.java$" \
                    > changed_files.txt || true

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

                    curl -X POST \
                        -F "file=@review.tar.gz" \
                        "$REVIEW_API" \
                        -o ai-review-result.json

                    cat ai-review-result.json
                '''
            }
        }
        stage('GitHub Status Check') {
            steps {withCredentials([
            string(
              credentialsId: 'github-token',
              variable: 'GITHUB_TOKEN'
            )
            ]) {

            sh '''
            curl \
            -X POST \
            -H "Authorization: token $GITHUB_TOKEN" \
            -H "Accept: application/vnd.github+json" \
            https://api.github.com/repos/PadmavathiVelmurugan/ai-code-review-poc/statuses/${GIT_COMMIT} \
            -d '{
              "state":"success",
              "description":"AI Code Review completed",
              "context":"AI Reviewer"
            }'
            '''

        }
    }
}
        

    }
}