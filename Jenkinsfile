pipeline {
    agent any

    environment {
        REVIEW_API = "http://docker.internal"
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
                    # Track changes on main branch via HEAD~1 since you are testing directly on main
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

                    # Safely package the source directory and our diff manifest
                    if [ -d "backend/src" ]; then
                        cp -r backend/src review_package/
                    fi
                    
                    if [ -f "backend/pom.xml" ]; then
                        cp backend/pom.xml review_package/
                    fi
                    
                    cp changed_files.txt review_package/

                    # Create a standard tarball instead of requiring the zip utility
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
                    ${REVIEW_API} \
                    -o ai-review-result.json

                    echo "========================================="
                    echo "AI Review Results Summary:"
                    echo "========================================="
                    cat ai-review-result.json
                '''
            }
        }
    }
}
