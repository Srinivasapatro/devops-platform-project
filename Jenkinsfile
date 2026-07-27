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

                    sh '''
                    git fetch --tags || true

                    LAST_TAG=$(git tag | grep '^v[0-9]*$' | sort -V | tail -1)

                    if [ -z "$LAST_TAG" ]; then
                        NEW_TAG=v1
                    else
                        NUM=${LAST_TAG#v}
                        NEW_TAG=v$((NUM+1))
                    fi

                    echo $NEW_TAG > image_tag.txt
                    '''

                    env.IMAGE_TAG = sh(
                        script: "cat image_tag.txt",
                        returnStdout: true
                    ).trim()

                    echo "New Docker Tag = ${env.IMAGE_TAG}"
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
                pytest
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build \
                    -t ${IMAGE_NAME}:${IMAGE_TAG} \
                    -t ${IMAGE_NAME}:latest \
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
                    docker push ${IMAGE_NAME}:latest

                    docker logout
                    '''
                }
            }
        }

        stage('Update Helm Values') {
            steps {

                sh '''
                sed -i "s/tag:.*/tag: ${IMAGE_TAG}/" \
                helm/devops-platform/values.yaml

                cat helm/devops-platform/values.yaml
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {

                sh '''
                helm upgrade --install ${HELM_RELEASE} ${HELM_CHART} \
                    -n ${K8S_NAMESPACE} \
                    --create-namespace

                kubectl rollout status deployment/devops-platform \
                    -n ${K8S_NAMESPACE}

                kubectl get pods -n ${K8S_NAMESPACE}
                '''
            }
        }

        stage('Create Git Tag') {
            steps {

                withCredentials([
                    usernamePassword(
                        credentialsId: 'github-creds',
                        usernameVariable: 'GITHUB_USER',
                        passwordVariable: 'GITHUB_TOKEN'
                    )
                ]) {

                    sh '''
                    git config user.name "Jenkins"
                    git config user.email "jenkins@local"

                    git tag ${IMAGE_TAG}

                    git push https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPOSITORY>.git ${IMAGE_TAG}
                    '''
                }
            }
        }
    }

    post {

        success {
            echo "======================================="
            echo "Build Successful"
            echo "Docker Image : ${IMAGE_NAME}:${IMAGE_TAG}"
            echo "Deployment Updated"
            echo "======================================="
        }

        failure {
            echo "======================================="
            echo "Build Failed"
            echo "======================================="
        }

        always {
            cleanWs()
        }
    }
}