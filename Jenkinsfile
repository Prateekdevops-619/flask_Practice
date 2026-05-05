pipeline {
    agent any

    environment {
        MONGO_URI = credentials('mongo-uri')
        SECRET_KEY = credentials('secret-key')
    }

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
                    python3 -m venv venv
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
                    # Stop any existing instance
                    pkill -f "python app.py" || true
                    # Start the app in the background on the staging port
                    nohup python app.py &
                    sleep 3
                    echo "Application deployed successfully on port 8000"
                '''
            }
        }
    }

    post {
        success {
            mail to: 'prateektiwari619@gmail.com',
                 subject: "SUCCESS: Pipeline '${env.JOB_NAME}' Build #${env.BUILD_NUMBER}",
                 body: """Build succeeded!

Job: ${env.JOB_NAME}
Build: #${env.BUILD_NUMBER}
URL: ${env.BUILD_URL}

Changes deployed to staging."""
        }
        failure {
            mail to: 'prateektiwari619@gmail.com',
                 subject: "FAILURE: Pipeline '${env.JOB_NAME}' Build #${env.BUILD_NUMBER}",
                 body: """Build failed!

Job: ${env.JOB_NAME}
Build: #${env.BUILD_NUMBER}
URL: ${env.BUILD_URL}

Please check the console output for details."""
        }
        always {
            cleanWs()
        }
    }
}
