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
                    pip3 install --upgrade pip --break-system-packages --quiet
                    pip3 uninstall bson -y 2>/dev/null || true
                    pip3 install -r requirements.txt --break-system-packages --quiet
                    pip3 install pytest --break-system-packages --quiet
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
            steps {
                sh '''
                    echo "Deploying to staging environment..."
                    pkill -f "python3 app.py" || true
                    export MONGO_URI="mongodb://localhost:27017/students"
                    export SECRET_KEY="staging-secret-key"
                    nohup python3 app.py > app.log 2>&1 &
                    sleep 5
                    if curl -s --max-time 5 http://localhost:8000 > /dev/null; then
                        echo "Application is running on port 8000"
                    else
                        echo "Warning: App may still be starting. Check app.log for details."
                        cat app.log || true
                    fi
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
