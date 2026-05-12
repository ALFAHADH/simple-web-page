pipeline {
    agent any

    environment {
        APP_NAME       = 'simple-web-page'                        // ✏️ CHANGE: your app name
        DOCKER_IMAGE   = 'alfahadh/simple-web-page'              // ✏️ CHANGE: your-dockerhub-username/your-image-name
        IMAGE_TAG      = "${BUILD_NUMBER}"                     // ✅ NO CHANGE: auto-increments
        CONTAINER_NAME = 'simple-web-page'                       // ✏️ CHANGE: your container name
        APP_PORT       = '5000'                                // ✏️ CHANGE: your app port
    }

    stages {

        // ─────────────────────────────────
        // STAGE 1: GIT CLONE
        // ─────────────────────────────────
        stage('Git Clone') {
            steps {
                echo "📥 Cloning repository..."
                git branch: 'main',                            // ✏️ CHANGE: your branch name (main/master)
                    url: 'https://github.com/alfahadh/simple-web-page.git'  // ✏️ CHANGE: your GitHub repo URL
                echo "✅ Code cloned successfully"
                echo "📌 Commit: ${env.GIT_COMMIT.take(7)}"   // ✅ NO CHANGE: auto picks git commit
                sh 'ls -la'
            }
        }

        // ─────────────────────────────────
        // STAGE 2: BUILD
        // ─────────────────────────────────
        stage('Build') {
            steps {
                echo "🔨 Installing dependencies..."
                sh 'pip install -r requirements.txt'           // ✅ NO CHANGE: reads your requirements.txt
                echo "✅ Dependencies installed"
            }
        }

        // ─────────────────────────────────
        // STAGE 3: TEST
        // ─────────────────────────────────
        stage('Test') {
            steps {
                echo "🧪 Running unit tests..."
                sh 'pip install pytest'                        // ✅ NO CHANGE
                sh 'pytest test_app.py -v --tb=short'         // ✏️ CHANGE: your test file name
                echo "✅ All tests passed!"
            }
        }

        // ─────────────────────────────────
        // STAGE 4: DOCKER BUILD & PUSH
        // ─────────────────────────────────
        stage('Docker Build & Push') {
            steps {
                echo "🐳 Building Docker image..."
                sh "docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} ."   // ✅ NO CHANGE: uses env vars above
                sh "docker tag ${DOCKER_IMAGE}:${IMAGE_TAG} ${DOCKER_IMAGE}:latest" // ✅ NO CHANGE
                echo "✅ Docker image built: ${DOCKER_IMAGE}:${IMAGE_TAG}"

                echo "📤 Pushing to DockerHub..."
                withCredentials([usernamePassword(
                    credentialsId: 'cred-id',          // ✏️ CHANGE: must match the ID you set in Jenkins Credentials Store
                    usernameVariable: 'DOCKER_USER',           // ✅ NO CHANGE: this is just a variable name
                    passwordVariable: 'DOCKER_PASS'            // ✅ NO CHANGE: this is just a variable name
                )]) {
                    sh """
                        echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin  // ✅ NO CHANGE
                        docker push ${DOCKER_IMAGE}:${IMAGE_TAG}   // ✅ NO CHANGE
                        docker push ${DOCKER_IMAGE}:latest         // ✅ NO CHANGE
                        docker logout                              // ✅ NO CHANGE
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
                    docker stop ${CONTAINER_NAME} || true      // ✅ NO CHANGE: uses env var above
                    docker rm   ${CONTAINER_NAME} || true      // ✅ NO CHANGE: uses env var above

                    docker pull ${DOCKER_IMAGE}:${IMAGE_TAG}   // ✅ NO CHANGE: uses env vars above

                    docker run -d \
                        --name ${CONTAINER_NAME} \             // ✅ NO CHANGE
                        --restart always \                     // ✅ NO CHANGE
                        -p ${APP_PORT}:5000 \                  // ✏️ CHANGE: 5000 = port inside container (must match your app)
                        ${DOCKER_IMAGE}:${IMAGE_TAG}           // ✅ NO CHANGE

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
                    curl -f http://localhost:${APP_PORT}/health && \  // ✏️ CHANGE: /health = your health endpoint
                        echo "✅ App is healthy!" || \
                        echo "⚠️ Health check failed!"
                """
                sh "docker ps | grep ${CONTAINER_NAME}"        // ✅ NO CHANGE
            }
        }
    }

    post {
        success {
            echo """
            ╔══════════════════════════════════════╗
            ║   ✅ PIPELINE SUCCESS                ║
            ║   Build : #${BUILD_NUMBER}
            ║   Image : ${DOCKER_IMAGE}:${IMAGE_TAG}
            ║   URL   : http://localhost:${APP_PORT}
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
            sh 'docker image prune -f || true'                 // ✅ NO CHANGE: cleans unused images
            cleanWs()                                          // ✅ NO CHANGE: cleans workspace
        }
    }
}
