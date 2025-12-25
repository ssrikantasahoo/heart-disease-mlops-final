# Heart Disease Prediction MLOps Pipeline

This project implements an end-to-end MLOps pipeline for predicting heart disease risk. It includes data ingestion, preprocessing, model training, experiment tracking, automated testing, containerization, and Kubernetes deployment.

## � Prerequisites

- **Python 3.9+**
- **Docker Desktop** (with Kubernetes enabled)
- **Git**

## ⚡ Quick Start

For a detailed walkthrough, see the [Deployment Guide](docs/DEPLOYMENT_GUIDE.md).

**Fast Track Local Deployment:**
1. `docker build -t heart-api .`
2. `docker build -f Dockerfile.ui -t heart-ui .`
3. `kubectl apply -f k8s/`
4. Access UI at [http://localhost:30081](http://localhost:30081)

## � Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd heart-disease-mlops-final
   ```

2. **Create and activate a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🛠️ Running the Pipeline

Execute the following scripts in order to prepare data and train models.

1. **Data Acquisition:**
   Downloads the dataset from UCI.
   ```bash
   python src/data_acquisition.py
   ```

2. **Preprocessing:**
   Cleans and encodes the data.
   ```bash
   python src/preprocessing.py
   ```

3. **Model Training:**
   Trains Logistic Regression and Random Forest models, performs cross-validation, and outputs a comparison table.
   ```bash
   python src/train.py
   ```

4. **Experiment Tracking:**
   Runs the training with MLflow tracking (metrics, params, artifacts).
   ```bash
   python src/experiment_tracking.py
   ```
   *View results by running `mlflow ui` and navigating to http://localhost:5000*
## 🐳 Docker Deployment

1. **Build the Docker image:**
   ```bash
   docker build -t heart-api .
## ☸️ Kubernetes Deployment

1. **Update Deployment Manifest:**
   Edit `k8s/deployment.yaml` and replace `<REPLACE_RUN_ID>` with your actual MLflow Run ID.

2. **Deploy to Cluster:**
   ```bash
   kubectl apply -f k8s/
   ```

3. **Verify Deployment:**
   ```bash
   kubectl get pods
   kubectl get services
   ```

4. **Access the Service:**
   The service is exposed via NodePort on port `30080`.
   - URL: `http://localhost:30080`
   - Metrics: `http://localhost:30080/metrics`

5. **Access the UI:**
   The user interface is exposed on port `30081`.
   - URL: `http://localhost:30081`

## � Monitoring

Prometheus is configured to scrape metrics from the API.
- Config file: `monitoring/prometheus.yml`
- Run Prometheus (using Docker):
  ```bash
  docker run -p 9090:9090 -v $(pwd)/monitoring/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus
  ```
- Access Prometheus UI at `http://localhost:9090`.

## 🚀 CI/CD and AWS Deployment

This project uses GitHub Actions for Continuous Integration and Continuous Deployment.

### 1. CI Pipeline (`.github/workflows/ci.yml`)
- Runs on every push and pull request to `main`.
- Installs dependencies, runs linting (`flake8`), and executes tests (`pytest`).

### 2. CD Pipeline (`.github/workflows/cd.yml`)
- Runs on every push to `main` (after CI passes).
- Builds the Docker image and pushes it to Amazon ECR.
- Can optionally deploy to AWS App Runner or ECS (requires uncommenting the deployment step in `cd.yml`).

### 3. AWS Configuration
To enable the CD pipeline, you must configure the following **Secrets** in your GitHub repository settings:

| Secret Name | Description |
|---|---|
| `AWS_ACCESS_KEY_ID` | Your AWS Access Key ID |
| `AWS_SECRET_ACCESS_KEY` | Your AWS Secret Access Key |
| `AWS_REGION` | AWS Region (e.g., `us-east-1`) |
| `ECR_REPOSITORY` | Name of your ECR repository (e.g., `heart-disease-mlops`) |
| `AWS_APP_RUNNER_SERVICE` | (Optional) Name of your App Runner service |

### 4. Local Configuration (.env)
A `.env` file has been created to store your AWS credentials locally. **DO NOT COMMIT THIS FILE** if it contains real keys. Use it for local testing or reference.