# Health Monitoring System

A production-grade cloud-based health monitoring application deployed on Microsoft Azure using Docker and Azure Container Instances.

## Overview

This system allows healthcare professionals to submit and track patient vitals in real time. It automatically flags abnormal readings as warnings or critical alerts, enabling faster response to patient health changes.

## Features

- Submit patient vitals including heart rate, blood pressure, and temperature
- Automatic status classification: Normal, Warning, and Critical
- Real-time patient records dashboard
- Containerized deployment using Docker
- Hosted on Azure Container Instances with public URL
- Automated CI/CD pipeline using GitHub Actions

## Tech Stack

- **Backend:** Python, Flask
- **Containerization:** Docker, Azure Container Registry
- **Cloud:** Microsoft Azure Container Instances
- **CI/CD:** GitHub Actions
- **Monitoring:** Azure Application Insights compatible logging

## Architecture
```
GitHub Push → GitHub Actions CI/CD → Docker Build → Azure Container Registry → Azure Container Instances → Live App
```

## Live Demo

http://nithish-health-monitor.eastus.azurecontainer.io:5000

## Setup and Installation

### Prerequisites
- Docker
- Azure CLI
- Python 3.9+

### Run Locally
```bash
git clone https://github.com/nithishbijadirajeev-droid/health-monitoring-system.git
cd health-monitoring-system
docker-compose up --build
```

Visit http://localhost:5001

### Deploy to Azure
```bash
az login
az acr login --name nithishealthmonitor
docker buildx build --platform linux/amd64 -t nithishealthmonitor.azurecr.io/health-monitoring-system:latest --push .
az container create --resource-group health-monitoring-rg --name health-monitoring-app --image nithishealthmonitor.azurecr.io/health-monitoring-system:latest --dns-name-label nithish-health-monitor --ports 5000 --os-type Linux --cpu 1 --memory 1.5
```

## Status Classification

| Status | Heart Rate | Temperature |
|--------|-----------|-------------|
| Normal | 60-100 bpm | Below 99.5F |
| Warning | Below 60 or above 100 bpm | Above 99.5F |
| Critical | Above 120 bpm | Above 103F |
