pipeline {
    agent any

    environment {
        IMAGE_NAME = "myapp"
    }

    stages {
        stage('Clone repository') {
            steps {
                git 'https://github.com/MukeshAnbazhagan / my-docker-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Run Docker Container') {
            steps {
                sh '''
                    docker stop my-container || true
                    docker rm my-container || true
                    docker run -d --name my-container -p 8000:8080 $IMAGE_NAME
                '''
            }
        }
    }
}
