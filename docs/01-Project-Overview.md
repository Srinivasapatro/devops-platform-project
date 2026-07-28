DevOps Platform Project
Project Summary

This project demonstrates an end-to-end DevOps pipeline for deploying and monitoring a Flask-based web application using modern DevOps tools and best practices.

The project includes:

Git & GitHub
Docker
Jenkins
Kubernetes
Helm
Prometheus
Grafana
Pytest
Docker Hub
Project Objective

Build a production-style CI/CD pipeline that automatically:

Builds the application
Runs unit tests
Builds Docker image
Pushes Docker image to Docker Hub
Updates Helm chart
Deploys to Kubernetes
Performs rolling update
Exposes Prometheus metrics
Visualizes metrics in Grafana
Project Architecture
Developer

      │

      ▼

GitHub Repository

      │

      ▼

Jenkins Pipeline

      │

      ├── Checkout Code

      ├── Install Dependencies

      ├── Run Pytest

      ├── Build Docker Image

      ├── Push Image to Docker Hub

      ├── Update Helm Values

      ├── Deploy using Helm

      ▼

Kubernetes Cluster

      │

      ▼

Flask Application

      │

      ├── /

      ├── /health

      └── /metrics

      │

      ▼

Prometheus

      │

      ▼

Grafana Dashboard
Tech Stack
Category	Tool
Source Control	Git
Repository	GitHub
CI/CD	Jenkins
Language	Python
Framework	Flask
Testing	Pytest
Containerization	Docker
Registry	Docker Hub
Orchestration	Kubernetes
Package Manager	Helm
Monitoring	Prometheus
Dashboard	Grafana
Features
CI/CD Automation
Rolling Deployment
Docker Image Versioning
Helm Deployment
Application Monitoring
Prometheus Metrics
Grafana Dashboards
Health Checks
Unit Testing
Application Endpoints
Endpoint	Purpose
/	Home Page
/health	Health Check
/metrics	Prometheus Metrics
Deployment Flow
Code Change

↓

Git Push

↓

Jenkins Build

↓

Run Tests

↓

Docker Build

↓

Docker Push

↓

Helm Upgrade

↓

Kubernetes Rolling Update

↓

Prometheus Scrapes Metrics

↓

Grafana Displays Dashboard
Skills Demonstrated
Git
GitHub
Jenkins
Docker
Docker Hub
Kubernetes
Helm
Flask
Python
Linux
Bash
YAML
Prometheus
Grafana
CI/CD
Monitoring