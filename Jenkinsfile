pipeline {
    agent any

    environment {
        IMAGE_NAME = "srinivasps/devops-platform"
        K8S_NAMESPACE = "devops-platform"
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

                    def lastTag = sh(
                        script: '''
                        git fetch --tags
                        git tag | grep '^v[0-9]*$' | sort -V | tail -1 || true
                        ''',
                        returnStdout: true
                    ).trim()

                    if (lastTag == "") {
                        env.IMAGE_TAG = "v1"
                    } else {
                        def version = lastTag.replace("v","").toInteger() + 1
                        env.IMAGE_TAG = "v${version}"
                    }

                    echo "New Docker Tag = ${env.IMAGE_TAG}"
                }
            }
        }

        stage('Debug Workspace') {
            steps {
                sh '''
                pwd

                echo "========================="
                ls -la
                echo "========================="

                ls -la app

                echo "========================="
                python3 -c "
import os
import sys

print('PWD =', os.getcwd())
print('PYTHONPATH =', os.getenv('PYTHONPATH'))
print('sys.path =')

for p in sys.path:
    print(p)
"
                '''
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

                export PYTHONPATH=$(pwd)

                python -m pytest -v
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
                sed -i "s/tag:.*/tag: ${IMAGE_TAG}/" \
                helm/devops-platform/values.yaml

                cat helm/devops-platform/values.yaml
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                helm upgrade --install \
                devops-platform \
                ./helm/devops-platform \
                -n ${K8S_NAMESPACE} \
                --create-namespace

                kubectl rollout status deployment/devops-platform \
                -n ${K8S_NAMESPACE}
                '''
            }
        }

        stage('Create Git Tag') {

            steps {

                withCredentials([
                    usernamePassword(
                        credentialsId: 'github-creds',
                        usernameVariable: 'GIT_USERNAME',
                        passwordVariable: 'GIT_PASSWORD'
                    )
                ]) {

                    sh '''

                    git config user.email "jenkins@local"

                    git config user.name "Jenkins"

                    git add helm/devops-platform/values.yaml

                    git commit -m "Release ${IMAGE_TAG}" || true

                    git tag ${IMAGE_TAG}

                    git push https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/srinivasps/devops-platform-project.git HEAD:main

                    git push https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/srinivasps/devops-platform-project.git ${IMAGE_TAG}

                    '''
                }
            }
        }
    }

    post {

        success {

            echo "======================================"
            echo "Build Successful"
            echo "Docker Image : ${IMAGE_NAME}:${IMAGE_TAG}"
            echo "======================================"

            cleanWs()
        }

        failure {

            echo "======================================"
            echo "Build Failed"
            echo "======================================"

            cleanWs()
        }
    }
}