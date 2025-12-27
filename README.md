# Heart Disease Prediction MLOps Pipeline

[![CI Pipeline](https://github.com/ssrikantasahoo/heart-disease-mlops-final/actions/workflows/ci.yml/badge.svg)](https://github.com/ssrikantasahoo/heart-disease-mlops-final/actions)
[![CD Pipeline](https://github.com/ssrikantasahoo/heart-disease-mlops-final/actions/workflows/cd.yml/badge.svg)](https://github.com/ssrikantasahoo/heart-disease-mlops-final/actions)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Docker](https://img.shields.io/badge/docker-available-blue.svg)](https://www.docker.com/)

An end-to-end MLOps solution for predicting heart disease risk. This project demonstrates a production-grade machine learning pipeline integrating automated training, experiment tracking, containerization, and Kubernetes-based deployment.

---

## 📌 Project Overview

The **Heart Disease MLOps Pipeline** is designed to streamline the lifecycle of a machine learning model from data ingestion to production deployment.
*   **Problem**: Early detection of heart disease can save lives. This project builds a predictive model using patient health metrics.
*   **Solution**: A robust, automated pipeline that trains Logistic Regression and Random Forest models, selects the best performer, and serves it via a scalable REST API.
*   **Key Features**:
    *   **Automated Pipeline**: Scripts for data acquisition, cleaning, training, and packaging.
    *   **Experiment Tracking**: Integrated with **MLflow** to track metrics, parameters, and artifacts.
    *   **Containerization**: Dockerized API and UI for consistent deployment.
    *   **Orchestration**: Kubernetes manifests for scalable production deployment.
    *   **Monitoring**: Prometheus metrics for real-time API health tracking.
    *   **CI/CD**: GitHub Actions for automated testing and deployment to AWS.


![Architecture Diagram](docs/image-1.png)

---

## 🏗️ Architecture & Technology Stack

*   **Language**: Python 3.9
*   **ML Frameworks**: Scikit-Learn, Pandas, NumPy
*   **Tracking**: MLflow
*   **API Framework**: FastAPI
*   **Containerization**: Docker
*   **Orchestration**: Kubernetes
*   **CI/CD**: GitHub Actions (Linting with Flake8, Testing with Pytest)
*   **Cloud Target**: AWS (ECR, App Runner/ECS support)

---

## 🚀 Getting Started

### Prerequisites
*   **Python 3.9+**
*   **Docker Desktop** (Kubernetes enabled)
*   **Git**

### 1. Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/ssrikantasahoo/heart-disease-mlops-final.git
cd heart-disease-mlops-final

# Create virtual environment (Optional)
python -m venv venv
# Windows: .\venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Running the ML Pipeline Locally

Execute the pipeline stages in sequence:

1.  **Data Acquisition**: `python src/data_acquisition.py`
    *   *Downloads dataset from UCI repository.*
2.  **Preprocessing**: `python src/preprocessing.py`
    *   *Cleans data, imputes missing values, encodes categories.*
3.  **Model Training**: `python src/train.py`
    *   *Trains models, performs GridSearch, selects best model.*
4.  **Experiment Tracking**: `python src/experiment_tracking.py`
    *   *Logs runs to MLflow. View UI at http://localhost:5000.*

---

## 🐳 Deployment Guide

For a detailed walkthrough, see [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md).

### Quick Local Deployment (Docker & K8s)

1.  **Build Custom Images**:
    ```bash
    docker build -t heart-api .
    docker build -f Dockerfile.ui -t heart-ui .
    ```
2.  **Deploy to Kubernetes**:
    ```bash
    kubectl apply -f k8s/
    ```
3.  **Access Services**:
    *   **Prediction UI**: [http://localhost:30081](http://localhost:30081)
    *   **API Docs**: [http://localhost:30080/docs](http://localhost:30080/docs)
    *   **Prometheus Monitoring**: [http://localhost:30090](http://localhost:30090)

---

## 🧪 Testing & Validation

### Pipeline Demo
Watch the pipeline in action (MLflow Experiment Tracking):

![Pipeline Demo](docs/pipeline_full.gif)

### Performance & Metrics
The pipeline compares **Logistic Regression** vs **Random Forest**.
*   **Metrics**: Accuracy, Precision, Recall, F1-Score.
*   **Visualization**: Confusion Matrices and ROC Curves are logged in MLflow.

---

## 🤝 CI/CD Workflows

This project uses **GitHub Actions** to automate quality checks and deployment.

### 1. CI Pipeline (`ci.yml`)
*   **Triggers**: Push/PR to `main`.
*   **Steps**: Linting (`flake8`), Unit Tests (`pytest`), Integration Test (Dry run of training).

### 2. CD Pipeline (`cd.yml`)
*   **Triggers**: Push to `main` (after successful CI).
*   **Steps**: Builds Docker image, pushes to **Amazon ECR**.

![CI/CD Workflow](docs/image-2.png)

---

## 📂 Project Structure

```
heart-disease-mlops-final/
├── .github/workflows/   # CI/CD definitions
├── data/                # Dataset storage
├── docs/                # Documentation & Artifacts
├── k8s/                 # Kubernetes manifests (deploy, service, ingress)
├── models/              # Serialized models
├── notebooks/           # EDA and experiments
├── src/                 # Source code
│   ├── app.py           # FastAPI application
│   ├── train.py         # Training script
│   └── ...
├── tests/               # Unit tests
├── ui/                  # HTML Frontend
├── Dockerfile           # API Docker config
├── Dockerfile.ui        # UI Docker config
└── requirements.txt     # Dependencies
```

---

## 📜 License
**Copyright © 2025. All Rights Reserved.**

This software is proprietary. unauthorized use, reproduction, distribution, or modification of this project, or any portion of it, is strictly prohibited without the prior written permission of the owner.
