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
                    python3 -m venv venv || python -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . venv/bin/activate
                    python -m pytest test_app.py -v --tb=short
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
                    . venv/bin/activate
                    pkill -f "python app.py" || true
                    nohup python app.py &
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
