pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = 'ai-tutor-chatbot'
    }

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Validate Environment') {
            steps {
                sh '''
                    test -f .env || {
                      echo ".env 파일이 없습니다. 서버에 운영용 .env를 먼저 배치하세요."
                      exit 1
                    }
                    docker compose config >/dev/null
                '''
            }
        }

        stage('Build Images') {
            steps {
                sh 'docker compose build --pull'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker compose up -d
                    docker compose ps
                '''
            }
        }

        stage('Post Deploy Check') {
            steps {
                sh '''
                    sleep 10
                    docker compose ps
                    docker compose logs backend --tail=50
                '''
            }
        }
    }

    post {
        success {
            sh 'docker image prune -f || true'
        }
        failure {
            sh 'docker compose logs --tail=100 || true'
        }
    }
}
