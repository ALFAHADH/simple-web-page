pipeline {
    agent any

    stages {
        stage('Deploy to EC2') {
            steps {
                sshagent(['da0a1480-55b8-45ea-8166-19aae75b0066']) {
                    sh """
                        scp -o StrictHostKeyChecking=no index.html ec2-user@65.2.78.245:/var/www/html/
                    """
                }
            }
        }
    }
}
