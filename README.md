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
    *   **Automated Pipeline**: Cross-platform script (`run_local_pipeline.py`) for complete ML workflow.
    *   **Dynamic Model Loading**: Automatically discovers and loads the latest trained model.
    *   **Auto-Training**: Trains models on first startup if none exist (Docker/K8s ready).
    *   **Experiment Tracking**: Integrated with **MLflow** to track metrics, parameters, and artifacts.
    *   **Containerization**: Dockerized API and UI for consistent deployment.
    *   **Orchestration**: Kubernetes manifests for scalable production deployment.
    *   **Monitoring**: Prometheus metrics for real-time API health tracking.
    *   **CI/CD**: GitHub Actions for automated testing and deployment to AWS.


![Architecture Diagram](docs/images/SystemArchitectureOverview.png)

![Data Flow Diagram](docs/images/DataFlowArchitecture.png)



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

Execute the complete pipeline with a single command:

```bash
python run_local_pipeline.py
```

![ML Training Pipeline](docs/images/MLTrainingPipeline.png)


This cross-platform script (works on Windows, Linux, and Mac) runs all pipeline stages:
1.  **Data Acquisition** - Downloads dataset from UCI repository
2.  **Preprocessing** - Cleans data, imputes missing values, encodes categories
3.  **Model Training** - Trains models, performs GridSearch, selects best model
4.  **Experiment Tracking** - Logs runs to MLflow (view UI at http://localhost:5000)
5.  **Model Packaging** - Packages the best model for deployment
6.  **Unit Tests** - Validates all components

**Or run individual stages:**
```bash
python src/data_acquisition.py
python src/preprocessing.py
python src/train.py
python src/experiment_tracking.py
```

---

## 🐳 Deployment Guide

For detailed deployment instructions:
- **Local Development**: [docs/LOCAL_DEPLOYMENT_GUIDE.md](docs/LOCAL_DEPLOYMENT_GUIDE.md)
- **Kubernetes**: [docs/KUBERNETES_DEPLOYMENT.md](docs/KUBERNETES_DEPLOYMENT.md)
- **CONFIGURATION**: [docs/CONFIGURATION_GUIDE.md](docs/CONFIGURATION_GUIDE.md)
- **PROMETHEUS**: [docs/PROMETHEUS_DASHBOARD.md](docs/PROMETHEUS_DASHBOARD.md)

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
    *   **MLflow UI**: [http://localhost:30050](http://localhost:30050)
    *   **Prometheus Monitoring**: [http://localhost:30090](http://localhost:30090)

---

## 🧪 Testing & Validation

### Pipeline Demo
Watch the pipeline in action (MLflow Experiment Tracking):

![Pipeline Demo](docs/images/pipeline_full.gif)

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

![CI/CD Workflow](docs/images/CICDPipelineArchitecture.png)

![Component Interaction Diagram](docs/images/ComponentInteractionDiagram.png)

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
