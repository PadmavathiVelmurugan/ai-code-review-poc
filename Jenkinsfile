pipeline {

    agent any

<<<<<<< HEAD
    environment {

          REVIEW_API = "http://host.docker.internal:8001/review"

    }

    stages {

        stage('Checkout') {

            steps {

                checkout scm

            }

        }


        // Replace your old Git Diff stage here
        stage('Git Diff') {

            steps {

                sh '''
                    git diff origin/main HEAD --name-only \
                    | grep "\\.java$" \
                    > changed_files.txt || true

                    echo "Changed Java Files"

                    cat changed_files.txt
=======
    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Backend') {
            steps {
                dir('backend') {
                    sh 'ls'
                }
            }
        }

        stage('Frontend') {
            steps {
                dir('frontend') {
                    sh 'ls'
                }
            }
        }

        stage('AI Review') {
            steps {
                sh '''
                curl http://host.docker.internal:8001/docs
>>>>>>> 02b3dc3087e17da5833c1d6c60ed3b38a6e7dc40
                '''
            }
        }

<<<<<<< HEAD

        stage('Build') {

            steps {
                 dir('backend')
                 {

                sh 'mvn clean package'
                 }

            }

        }


        stage('SonarQube') {

            steps {

                sh '''
                    mvn sonar:sonar \
                    -Dsonar.projectKey=ai-code-review \
                    -Dsonar.host.url=http://host.docker.internal:9000 \
                    -Dsonar.login=sqa_fc602301ca8dff7462735bd05ffb8749c935f429
                '''

            }

        }


        stage('Create Review ZIP') {

            steps {

                sh '''
                    mkdir review_package

                    cp -r backend/src review_package/
                    cp backend/pom.xml review_package/
                    cp changed_files.txt review_package/

                    cd review_package

                    zip -r ../review.zip .
                     '''

            }

        }


        stage('AI Code Review') {

            steps {

                sh '''
                   curl -X POST \
                   -F "file=@review.zip" \
                   http://host.docker.internal:8001/review \
                   -o ai-review-result.json


                  echo "AI Review Result:"
                  cat ai-review-result.json
                 '''

            }

        }

    }

=======
    }
>>>>>>> 02b3dc3087e17da5833c1d6c60ed3b38a6e7dc40
}