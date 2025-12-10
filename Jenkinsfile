pipeline {
    agent {
        docker {
            image 'docker:latest'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
        IMAGE = "localhost:5000/simple-webapp"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git 'https://github.com/ALFAHADH/simple-web-page.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t $IMAGE:latest .
                '''
            }
        }

        stage('Push to Local Registry') {
            steps {
                sh '''
                docker push $IMAGE:latest
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KCFG')]) {
                    sh '''
                    export KUBECONFIG=$KCFG
                    
                    kubectl apply -f deployment.yaml
                    kubectl rollout restart deployment/webapp
                    '''
                }
            }
        }
    }
}
