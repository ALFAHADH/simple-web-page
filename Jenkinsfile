pipeline {
    agent any

    environment {
        APP_NAME       = 'simple-web-page'
        DOCKER_IMAGE   = 'alfahadh/simple-web-page'
        IMAGE_TAG      = "${BUILD_NUMBER}"
        CONTAINER_NAME = 'simple-web-page'
        APP_PORT       = '5000'
    }

    stages {

        stage('Git Clone') {
            steps {
                echo "📥 Cloning repository..."
                git branch: 'main',
                    url: 'https://github.com/alfahadh/simple-web-page.git'

                echo "✅ Code cloned successfully"
                sh 'ls -la'
            }
        }

        stage('Build') {
            steps {
                echo "🔨 Installing dependencies..."
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                echo "🧪 Running tests..."
                sh 'pip install pytest'
                sh 'pytest test_app.py -v --tb=short'
            }
        }

        stage('Docker Build & Push') {
            steps {

                sh "docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} ."

                sh "docker tag ${DOCKER_IMAGE}:${IMAGE_TAG} ${DOCKER_IMAGE}:latest"

                withCredentials([usernamePassword(
                    credentialsId: 'cred-id',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {

                    sh """
                        echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin
                        docker push ${DOCKER_IMAGE}:${IMAGE_TAG}
                        docker push ${DOCKER_IMAGE}:latest
                        docker logout
                    """
                }
            }
        }

        stage('Deploy') {
            steps {

                sh """
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true

                    docker pull ${DOCKER_IMAGE}:${IMAGE_TAG}

                    docker run -d \
                    --name ${CONTAINER_NAME} \
                    --restart always \
                    -p ${APP_PORT}:5000 \
                    ${DOCKER_IMAGE}:${IMAGE_TAG}
                """
            }
        }

        stage('Health Check') {
            steps {

                sh """
                    sleep 10
                    curl -f http://localhost:${APP_PORT}/health
                """

                sh "docker ps | grep ${CONTAINER_NAME}"
            }
        }
    }

    post {

        success {
            echo "✅ Pipeline completed successfully!"
        }

        failure {
            echo "❌ Pipeline failed!"
        }

        always {
            sh 'docker image prune -f || true'
            cleanWs()
        }
    }
}
