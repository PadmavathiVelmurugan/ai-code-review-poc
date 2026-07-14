pipeline {

    agent any

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
                '''
            }
        }

    }
}