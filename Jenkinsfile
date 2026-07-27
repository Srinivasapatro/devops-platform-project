pipeline {
    agent any

    environment {
        IMAGE_NAME = "srinivasps/devops-platform"
        IMAGE_TAG = "v1"
        K8S_NAMESPACE = "devops-platform"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verify Python') {
            steps {
                sh 'python3 --version'
            }
        }

        stage('Create Virtual Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    python -m pip install --upgrade pip
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    . venv/bin/activate
                    pip install -r app/requirements.txt
                    pip install pytest
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    python -m pytest
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ./app
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

                        docker push ${IMAGE_NAME}:${IMAGE_TAG}

                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl apply -f kubernetes/namespace.yaml
                    kubectl apply -f kubernetes/deployment.yaml
                    kubectl apply -f kubernetes/service.yaml

                    kubectl rollout restart deployment/devops-platform -n ${K8S_NAMESPACE}

                    kubectl rollout status deployment/devops-platform -n ${K8S_NAMESPACE}

                    kubectl get pods -n ${K8S_NAMESPACE}
                '''
            }
        }
    }

    post {

        success {
            echo '========================================='
            echo 'Pipeline completed successfully!'
            echo 'Application deployed to Kubernetes.'
            echo '========================================='
        }

        failure {
            echo '========================================='
            echo 'Pipeline failed.'
            echo '========================================='
        }

        always {
            cleanWs()
        }
    }
}