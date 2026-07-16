pipeline {
    agent any

    environment {
        REVIEW_API = "http://docker.internal"
        SONAR_TOKEN = "sqa_fc602301ca8dff7462735bd05ffb8749c935f429"
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

        stage('Build Backend') {
            steps {
                dir('backend') {
                    sh 'mvn clean package -DskipTests'
                }
            }
        }

        stage('SonarQube Static Analysis') {
            steps {
                dir('backend') {
                    sh """
                        mvn sonar:sonar \
                        -Dsonar.projectKey=ai-code-review \
                        -Dsonar.host.url=http://docker.internal \
                        -Dsonar.token=${SONAR_TOKEN}
                    """
                }
            }
        }

        stage('Package Review Artifacts') {
            steps {
                sh '''
                    rm -rf review_package review.zip
                    mkdir review_package

                    cp -r backend/src review_package/
                    cp backend/pom.xml review_package/
                    cp changed_files.txt review_package/

                    cd review_package
                    zip -r ../review.zip .
                '''
            }
        }

        stage('AI Code Review Execution') {
            steps {
                sh '''
                    echo "Sending review packet to AI Review Agent..."
                    
                    curl -X POST \
                    -F "file=@review.zip" \
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

