# DevOps Platform Project

A complete end-to-end DevOps project demonstrating CI/CD, Docker, Kubernetes, Jenkins, Prometheus, Grafana, Helm, and Terraform.

---

## Project Overview

This project demonstrates a modern DevOps workflow from source code to production deployment.

The application is a Python Flask REST API that is automatically built, tested, containerized, pushed to Docker Hub, and deployed to Kubernetes using Jenkins.

The application is monitored using Prometheus and Grafana.

---

## Features

- Python Flask REST API
- Docker containerization
- Kubernetes deployment
- Jenkins CI/CD Pipeline
- Automatic Docker image versioning
- Docker Hub integration
- Kubernetes rolling deployment
- Prometheus monitoring
- Grafana dashboards
- Pytest unit testing
- Helm chart support
- Terraform project structure

---

## Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Backend Application |
| Flask | REST API |
| Docker | Containerization |
| Jenkins | CI/CD Pipeline |
| Docker Hub | Image Registry |
| Kubernetes | Container Orchestration |
| Prometheus | Metrics Collection |
| Grafana | Visualization |
| Helm | Kubernetes Package Manager |
| Terraform | Infrastructure as Code |
| Git | Version Control |
| GitHub | Source Code Repository |

---

## Project Architecture

```
                    Developer
                        │
                        ▼
                 GitHub Repository
                        │
                        ▼
                Jenkins CI/CD Pipeline
        ┌───────────────┼────────────────┐
        ▼               ▼                ▼
   Run Unit Tests   Build Docker    Version Docker Image
                            │
                            ▼
                    Push Docker Hub
                            │
                            ▼
                  Kubernetes Deployment
                            │
                            ▼
                    Flask Application
                            │
             ┌──────────────┴──────────────┐
             ▼                             ▼
        Prometheus                    Grafana
```

---

## Project Workflow

1. Developer pushes code to GitHub.

2. Jenkins automatically starts the pipeline.

3. Jenkins performs:

- Checkout source code
- Install dependencies
- Run unit tests
- Build Docker image
- Push image to Docker Hub
- Update Kubernetes deployment
- Deploy latest version
- Verify rollout

4. Prometheus scrapes application metrics.

5. Grafana visualizes metrics.

---

## Folder Structure

```
devops-platform-project/
│
├── app/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── kubernetes/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── namespace.yaml
│
├── helm/
│
├── terraform/
│
├── tests/
│   └── test_app.py
│
├── monitoring/
│
├── screenshots/
│
├── Jenkinsfile
│
└── README.md
```

---

## Jenkins Pipeline

The Jenkins pipeline performs the following stages:

- Checkout Source Code
- Determine Docker Version
- Verify Python
- Create Virtual Environment
- Install Dependencies
- Run Unit Tests
- Build Docker Image
- Push Docker Image
- Update Kubernetes Deployment
- Deploy to Kubernetes

---

## Docker Image Versioning

Every successful Jenkins build automatically creates a new Docker image version.

Example:

```
v1
v2
v3
v4
v5
```

The Kubernetes deployment is automatically updated to use the latest image.

---

## Monitoring

Metrics are collected using Prometheus.

Example metrics:

- HTTP Request Count
- HTTP Request Rate
- Request Latency
- Process CPU Usage
- Process Memory Usage

Grafana dashboards visualize these metrics in real time.

---

## Testing

Unit testing is performed using Pytest.

Run tests locally:

```bash
export PYTHONPATH=$(pwd)
pytest -v
```

---

## Build Docker Image

```bash
docker build -t srinivasps/devops-platform:v1 ./app
```

---

## Push Docker Image

```bash
docker push srinivasps/devops-platform:v1
```

---

## Kubernetes Deployment

Deploy application:

```bash
kubectl apply -f kubernetes/
```

Check pods:

```bash
kubectl get pods -n devops-platform
```

Check deployment:

```bash
kubectl get deployment -n devops-platform
```

---

## Monitoring Stack

Port Forward Prometheus

```bash
kubectl port-forward svc/prometheus-server 9090:80 -n monitoring
```

Port Forward Grafana

```bash
kubectl port-forward svc/grafana 3000:80 -n monitoring
```

---

## Screenshots

Screenshots are available inside the `screenshots/` directory.

- Jenkins Pipeline
- Jenkins Stage View
- Docker Hub Repository
- Kubernetes Pods
- Kubernetes Deployment
- Prometheus Targets
- Grafana Dashboard
- Running Application

---

## Future Improvements

- GitHub Actions Pipeline
- SonarQube Integration
- Trivy Image Scanning
- ArgoCD GitOps
- Loki Logging
- Fluent Bit
- Terraform Infrastructure Deployment

---

## Author

**Srinivas**

DevOps Engineer

GitHub:
https://github.com/srinivasps/devops-platform-project
