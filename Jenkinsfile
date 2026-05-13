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

        // =========================================================
        // STAGE 1 : CLONE REPOSITORY
        // =========================================================
        stage('Git Clone') {

            steps {

                echo "📥 Cloning GitHub repository..."

                git branch: 'main',
                    url: 'https://github.com/ALFAHADH/simple-web-page.git'

                echo "✅ Repository cloned successfully"

                sh 'ls -la'
            }
        }

        // =========================================================
        // STAGE 2 : BUILD
        // =========================================================
        stage('Build') {

            steps {

                echo "🔨 Creating Python virtual environment..."

                sh '''
                    python3 -m venv venv

                    . venv/bin/activate

                    pip install --upgrade pip

                    pip install -r requirements.txt
                '''

                echo "✅ Dependencies installed successfully"
            }
        }

        // =========================================================
        // STAGE 3 : TEST
        // =========================================================
        stage('Test') {

            steps {

                echo "🧪 Running unit tests..."

                sh '''
                    . venv/bin/activate

                    pip install pytest

                    pytest test_app.py -v --tb=short
                '''

                echo "✅ All tests passed!"
            }
        }

        // =========================================================
        // STAGE 4 : DOCKER BUILD
        // =========================================================
        stage('Docker Build') {

            steps {

                echo "🐳 Building Docker image..."

                sh """
                    docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} .
                """

                sh """
                    docker tag ${DOCKER_IMAGE}:${IMAGE_TAG} ${DOCKER_IMAGE}:latest
                """

                echo "✅ Docker image built successfully"
            }
        }

        // =========================================================
        // STAGE 5 : DOCKER LOGIN & PUSH
        // =========================================================
        stage('Docker Push') {

            steps {

                echo "📤 Logging into DockerHub..."

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

                echo "✅ Docker image pushed successfully"
            }
        }

        // =========================================================
        // STAGE 6 : DEPLOY CONTAINER
        // =========================================================
        stage('Deploy') {

            steps {

                echo "🚀 Deploying container..."

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

                echo "✅ Container deployed successfully"
            }
        }

        // =========================================================
        // STAGE 7 : HEALTH CHECK
        // =========================================================
        stage('Health Check') {

            steps {

                echo "🏥 Running application health check..."

                sh """
                    sleep 10

                    curl -f http://localhost:${APP_PORT}/health
                """

                sh """
                    docker ps
                """

                echo "✅ Application is healthy"
            }
        }
    }

    // =========================================================
    // POST ACTIONS
    // =========================================================
    post {

        success {

            echo """
            ==================================================

            ✅ PIPELINE SUCCESSFUL

            App Name   : ${APP_NAME}
            Build No   : ${BUILD_NUMBER}
            Docker Img : ${DOCKER_IMAGE}:${IMAGE_TAG}

            Application URL:
            http://localhost:${APP_PORT}

            ==================================================
            """
        }

        failure {

            echo """
            ==================================================

            ❌ PIPELINE FAILED

            Build Number : ${BUILD_NUMBER}

            Check Jenkins console logs.

            ==================================================
            """
        }

        always {

            echo "🧹 Cleaning workspace..."

            sh 'docker image prune -f || true'

            cleanWs()
        }
    }
}
