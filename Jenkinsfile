pipeline {
    agent any

      environment {
        DOCKER_IMAGE = "ktmlover/voise-hospital-predictor"
        CONTAINER_NAME = "voise-hospital-container"
        PYTHON = "C:\\Python314\\python.exe"
    }

    stages {

        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Git Version Check') {
            steps {
                bat 'git --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '"%PYTHON%" -m pip install -r requirements.txt'
            }
        }

        stage('OWASP Dependency Check') {
            steps {
                dependencyCheck(
                    additionalArguments: '--scan . --format HTML --format XML --out dependency-check-report',
                    odcInstallation: 'OWASP-Dependency-Check'
                )
            }
        }

        stage('Publish OWASP Report') {
            steps {
                dependencyCheckPublisher(
                    pattern: 'dependency-check-report/dependency-check-report.xml'
                )
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    bat """
                        sonar-scanner ^
                        -Dsonar.projectKey=voise-hospital-predictor ^
                        -Dsonar.projectName="VOISE Hospital Predictor" ^
                        -Dsonar.sources=. ^
                        -Dsonar.inclusions=**/*.py ^
                        -Dsonar.exclusions=**/__pycache__/**,**/*.pyc
                    """
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                bat "docker build -t %DOCKER_IMAGE%:latest ."
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    bat """
                        docker login -u %DOCKER_USER% -p %DOCKER_PASS%
                        docker push %DOCKER_IMAGE%:latest
                        docker logout
                    """
                }
            }
        }

        stage('Deploy Container') {
            steps {
                bat "docker stop %CONTAINER_NAME% || exit 0"
                bat "docker rm %CONTAINER_NAME% || exit 0"
                bat "docker run -d --name %CONTAINER_NAME% -p 5001:5000 %DOCKER_IMAGE%:latest"
            }
        }
    }

    post {
        success {
            echo 'Pipeline  completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
        always {
            echo 'Post actions done.'
        }
    }
}
