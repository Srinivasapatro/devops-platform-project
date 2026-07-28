pipeline {
    agent any

    environment {
        IMAGE_NAME = "srinivasps/devops-platform"
        K8S_NAMESPACE = "devops-platform"
        HELM_RELEASE = "devops-platform"
        HELM_CHART = "./helm/devops-platform"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Determine Image Version') {
            steps {
                script {
                    env.IMAGE_TAG = "v${env.BUILD_NUMBER}"
                    echo "=================================="
                    echo "Docker Image Tag: ${env.IMAGE_TAG}"
                    echo "=================================="
                }
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

                export PYTHONPATH=$WORKSPACE

                pytest -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build \
                    -t ${IMAGE_NAME}:${IMAGE_TAG} \
                    ./app
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
                    echo "$DOCKER_PASSWORD" | docker login \
                        -u "$DOCKER_USERNAME" \
                        --password-stdin

                    docker push ${IMAGE_NAME}:${IMAGE_TAG}

                    docker logout
                    '''
                }
            }
        }

        stage('Update Helm Values') {
            steps {
                sh '''
                sed -i "s|repository:.*|repository: ${IMAGE_NAME}|" \
                    helm/devops-platform/values.yaml

                sed -i "s|tag:.*|tag: ${IMAGE_TAG}|" \
                    helm/devops-platform/values.yaml

                echo "========== values.yaml =========="
                cat helm/devops-platform/values.yaml
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                kubectl apply -f kubernetes/namespace.yaml

                helm upgrade --install \
                    ${HELM_RELEASE} \
                    ${HELM_CHART} \
                    -n ${K8S_NAMESPACE}

                kubectl rollout status deployment/devops-platform \
                    -n ${K8S_NAMESPACE}

                kubectl get pods -n ${K8S_NAMESPACE}
                '''
            }
        }
    }

    post {

        success {

            echo ""
            echo "========================================="
            echo "Build Successful"
            echo "Docker Image : ${IMAGE_NAME}:${IMAGE_TAG}"
            echo "Namespace    : ${K8S_NAMESPACE}"
            echo "========================================="
        }

        failure {

            echo ""
            echo "========================================="
            echo "Build Failed"
            echo "========================================="
        }

        always {

            cleanWs()
        }
    }
}