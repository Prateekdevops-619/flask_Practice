pipeline {
    agent any

    triggers {
        githubPush()
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Prateekdevops-619/flask_Practice.git'
            }
        }

        stage('Build') {
            steps {
                sh '''
                    pip3 install --upgrade pip --quiet
                    pip3 install -r requirements.txt --quiet
                    pip3 install pytest --quiet
                    echo "Dependencies installed successfully"
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    python3 -m pytest test_app.py -v --tb=short
                '''
            }
        }

        stage('Deploy to Staging') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                    echo "Deploying to staging environment..."
                    pkill -f "python3 app.py" || true
                    nohup python3 app.py &
                    sleep 3
                    echo "Application deployed on port 8000"
                '''
            }
        }
    }

    post {
        success {
            echo "Pipeline succeeded! Build #${env.BUILD_NUMBER} completed successfully."
        }
        failure {
            echo "Pipeline failed! Build #${env.BUILD_NUMBER} failed. Check console output: ${env.BUILD_URL}"
        }
    }
}
