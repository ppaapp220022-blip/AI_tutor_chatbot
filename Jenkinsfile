pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = 'ai_tutor_chatbot'
        DEPLOY_DIR = '/opt/ai_tutor_chatbot'
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
                    cd "$DEPLOY_DIR"
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
                sh '''
                    cd "$DEPLOY_DIR"
                    git pull origin main
                    docker compose build --pull
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    cd "$DEPLOY_DIR"
                    docker compose up -d
                    docker compose ps
                '''
            }
        }

        stage('Post Deploy Check') {
            steps {
                sh '''
                    cd "$DEPLOY_DIR"
                    sleep 10
                    docker compose ps
                    docker compose logs backend --tail=50
                '''
            }
        }
    }

    post {
        success {
            sh '''
                cd "$DEPLOY_DIR"
                docker image prune -f || true
            '''
        }
        failure {
            sh '''
                cd "$DEPLOY_DIR"
                docker compose logs --tail=100 || true
            '''
        }
    }
}