pipeline {
    agent any

    environment {
        APP_NAME     = 'my-flask-app'
        DOCKER_IMAGE = 'your-dockerhub-username/my-flask-app'
        IMAGE_TAG    = "${BUILD_NUMBER}"
        CONTAINER_NAME = 'my-flask-app'
        APP_PORT     = '5000'
    }

    stages {

        // ─────────────────────────────────
        // STAGE 1: GIT CLONE
        // ─────────────────────────────────
        stage('Git Clone') {
            steps {
                echo "📥 Cloning repository..."
                git branch: 'main',
                    url: 'https://github.com/your-username/my-app.git'
                echo "✅ Code cloned successfully"
                echo "📌 Commit: ${env.GIT_COMMIT.take(7)}"
                sh 'ls -la'
            }
        }

        // ─────────────────────────────────
        // STAGE 2: BUILD
        // ─────────────────────────────────
        stage('Build') {
            steps {
                echo "🔨 Installing dependencies..."
                sh 'pip install -r requirements.txt'
                echo "✅ Dependencies installed"
            }
        }

        // ─────────────────────────────────
        // STAGE 3: TEST
        // ─────────────────────────────────
        stage('Test') {
            steps {
                echo "🧪 Running unit tests..."
                sh 'pip install pytest'
                sh 'pytest test_app.py -v --tb=short'
                echo "✅ All tests passed!"
            }
        }

        // ─────────────────────────────────
        // STAGE 4: DOCKER BUILD & PUSH
        // ─────────────────────────────────
        stage('Docker Build & Push') {
            steps {
                echo "🐳 Building Docker image..."
                sh "docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} ."
                sh "docker tag ${DOCKER_IMAGE}:${IMAGE_TAG} ${DOCKER_IMAGE}:latest"
                echo "✅ Docker image built: ${DOCKER_IMAGE}:${IMAGE_TAG}"

                echo "📤 Pushing to DockerHub..."
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh """
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker push ${DOCKER_IMAGE}:${IMAGE_TAG}
                        docker push ${DOCKER_IMAGE}:latest
                        docker logout
                    """
                }
                echo "✅ Image pushed to DockerHub!"
            }
        }

        // ─────────────────────────────────
        // STAGE 5: DEPLOY
        // ─────────────────────────────────
        stage('Deploy') {
            steps {
                echo "🚀 Deploying ${APP_NAME}..."
                sh """
                    # Stop and remove existing container
                    docker stop ${CONTAINER_NAME} || true
                    docker rm   ${CONTAINER_NAME} || true

                    # Pull latest image and run
                    docker pull ${DOCKER_IMAGE}:${IMAGE_TAG}

                    docker run -d \
                        --name  ${CONTAINER_NAME} \
                        --restart always \
                        -p ${APP_PORT}:5000 \
                        ${DOCKER_IMAGE}:${IMAGE_TAG}

                    echo "✅ Container started!"
                """
            }
        }

        // ─────────────────────────────────
        // STAGE 6: HEALTH CHECK
        // ─────────────────────────────────
        stage('Health Check') {
            steps {
                echo "🏥 Running health check..."
                sh """
                    sleep 5
                    curl -f http://localhost:${APP_PORT}/health && \
                        echo "✅ App is healthy!" || \
                        echo "⚠️ Health check failed!"
                """
                sh "docker ps | grep ${CONTAINER_NAME}"
            }
        }
    }

    post {
        success {
            echo """
            ╔══════════════════════════════════════╗
            ║   ✅ PIPELINE SUCCESS                ║
            ║   Build    : #${BUILD_NUMBER}         
            ║   Image    : ${DOCKER_IMAGE}:${IMAGE_TAG}
            ║   App URL  : http://localhost:${APP_PORT}
            ╚══════════════════════════════════════╝
            """
        }
        failure {
            echo """
            ╔══════════════════════════════════════╗
            ║   ❌ PIPELINE FAILED                 ║
            ║   Build : #${BUILD_NUMBER}            
            ║   Check console logs for details     ║
            ╚══════════════════════════════════════╝
            """
        }
        always {
            // Clean dangling images to free disk space
            sh 'docker image prune -f || true'
            cleanWs()
        }
    }
}
