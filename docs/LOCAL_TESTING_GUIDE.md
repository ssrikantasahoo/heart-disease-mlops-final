# Local Testing Guide

Complete step-by-step instructions for running and accessing all components of the Heart Disease MLOps project locally.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Running the ML Pipeline](#running-the-ml-pipeline)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [Accessing All Services](#accessing-all-services)
6. [Testing the Application](#testing-the-application)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before starting, ensure you have the following installed:

- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **Docker Desktop** - [Download](https://www.docker.com/products/docker-desktop/)
- **Kubernetes** - Enable in Docker Desktop settings
- **Git** - [Download](https://git-scm.com/downloads)

### Verify Installations

```bash
# Check Python version
python --version

# Check Docker
docker --version

# Check Kubernetes
kubectl version --client

# Check Git
git --version
```

---

## Initial Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/ssrikantasahoo/heart-disease-mlops-final.git
cd heart-disease-mlops-final
```

### Step 2: Create Virtual Environment (Optional but Recommended)

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**Mac/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the ML Pipeline

The ML pipeline performs data acquisition, preprocessing, model training, and experiment tracking.

### Step 1: Run the Complete Pipeline

```bash
python run_local_pipeline.py
```

This script will:
1. ✅ Download the UCI Heart Disease dataset
2. ✅ Preprocess the data (handle missing values, encode features)
3. ✅ Train models (Logistic Regression and Random Forest)
4. ✅ Log experiments to MLflow
5. ✅ Package the best model
6. ✅ Run unit tests

**Expected Output:**
```
========================================
Starting Heart Disease MLOps Pipeline
========================================

Step 1: Data Acquisition
✓ Dataset downloaded successfully

Step 2: Data Preprocessing
✓ Data preprocessed and saved

Step 3: Model Training
✓ Models trained successfully
✓ Best model: RandomForestClassifier

Step 4: Experiment Tracking
✓ Experiments logged to MLflow

Step 5: Model Packaging
✓ Model packaged successfully

Step 6: Running Tests
✓ All tests passed

========================================
Pipeline completed successfully!
========================================
```

### Step 2: View MLflow Experiments

Start the MLflow UI to view experiment results:

```bash
mlflow ui
```

**Access MLflow:**
- **URL**: http://localhost:5000
- **What to see**: 
  - Experiment runs
  - Model metrics (Accuracy, Precision, Recall, F1-Score)
  - Confusion matrices
  - ROC curves
  - Model parameters

---

## Kubernetes Deployment

Deploy all services to Kubernetes for a production-like environment.

### Step 1: Build Docker Images

```bash
# Build API image
docker build -t heart-api .

# Build UI image
docker build -f Dockerfile.ui -t heart-ui .
```

### Step 2: Deploy to Kubernetes

```bash
# Apply all Kubernetes manifests
kubectl apply -f k8s/
```

**Expected Output:**
```
deployment.apps/heart-api-deployment created
configmap/grafana-datasources created
configmap/grafana-dashboards-config created
configmap/grafana-dashboard-heart-api created
deployment.apps/grafana created
service/grafana-service created
ingress.networking.k8s.io/heart-api-ingress created
deployment.apps/mlflow-ui-deployment created
service/mlflow-service created
configmap/prometheus-config created
deployment.apps/prometheus created
service/prometheus-service created
service/heart-api-service created
deployment.apps/heart-ui-deployment created
service/heart-ui-service created
```

### Step 3: Verify Deployments

```bash
# Check all pods are running
kubectl get pods

# Check all services
kubectl get services
```

**Wait for all pods to show `Running` status** (this may take 1-2 minutes).

---

## Accessing All Services

Once Kubernetes deployment is complete, access all services through your browser.

### 1. Prediction Web UI

**Access the user-friendly web interface for making predictions.**

- **URL**: http://localhost:30081
- **Purpose**: Interactive form to input patient data and get predictions
- **How to use**:
  1. Open http://localhost:30081 in your browser
  2. Fill in patient health metrics (age, blood pressure, cholesterol, etc.)
  3. Click "Predict" button
  4. View prediction result (Heart Disease Risk: Yes/No)

---

### 2. FastAPI Documentation

**Interactive API documentation with Swagger UI.**

- **URL**: http://localhost:30080/docs
- **Purpose**: Test API endpoints, view request/response schemas
- **How to use**:
  1. Open http://localhost:30080/docs
  2. Expand `/predict` endpoint
  3. Click "Try it out"
  4. Enter sample patient data:
     ```json
     {
       "age": 63,
       "sex": 1,
       "cp": 3,
       "trestbps": 145,
       "chol": 233,
       "fbs": 1,
       "restecg": 0,
       "thalach": 150,
       "exang": 0,
       "oldpeak": 2.3,
       "slope": 0,
       "ca": 0,
       "thal": 1
     }
     ```
  5. Click "Execute"
  6. View response

**Alternative API Endpoint:**
- **URL**: http://localhost:30080/redoc (ReDoc documentation)

---

### 3. MLflow UI

**Experiment tracking and model registry.**

- **URL**: http://localhost:30050
- **Purpose**: View experiment runs, compare models, track metrics
- **How to use**:
  1. Open http://localhost:30050
  2. Click on "Heart Disease Experiment"
  3. View all experiment runs
  4. Compare metrics across different runs
  5. View artifacts (confusion matrices, ROC curves)
  6. Download trained models

**Key Features:**
- Compare multiple runs side-by-side
- View hyperparameters
- Download model artifacts
- Track model versions

---

### 4. Prometheus Metrics

**Raw metrics collection and monitoring.**

- **URL**: http://localhost:30090
- **Purpose**: View raw Prometheus metrics, query data, check targets
- **How to use**:
  1. Open http://localhost:30090
  2. **View Targets**: Click "Status" → "Targets"
     - Verify `heart-api` target is "UP"
  3. **Query Metrics**: Go to "Graph" tab
     - Try query: `api_requests_total`
     - Try query: `up{job="heart-api"}`
     - Try query: `rate(api_requests_total[1m])`
  4. Click "Execute" to see results

**Available Metrics:**
- `api_requests_total` - Total API requests
- `up{job="heart-api"}` - API health status

---

### 5. Grafana Dashboard

**Rich visualization dashboards for monitoring.**

- **URL**: http://localhost:30300
- **Credentials**: 
  - Username: `admin`
  - Password: `admin`
- **Purpose**: Visual monitoring dashboards with real-time updates

**How to use:**

1. **Login**:
   - Navigate to http://localhost:30300
   - Enter username: `admin`
   - Enter password: `admin`
   - Click "Log in"
   - Skip password change (or change it)

2. **Access Dashboard**:
   - Click "Dashboards" (four squares icon) in left sidebar
   - Click "Browse"
   - Select "Heart Disease API Metrics"

3. **Dashboard Panels**:
   - **API Request Rate**: Requests per second over time
   - **Total API Requests**: Cumulative request count (gauge)
   - **API Health Status**: Green (Up) or Red (Down)
   - **Cumulative Requests Over Time**: Historical trend line

4. **Dashboard Features**:
   - Auto-refreshes every 5 seconds
   - Shows last 15 minutes of data by default
   - Adjust time range in top-right corner
   - Hover over graphs for detailed values

---

## Testing the Application

### Test 1: Make a Prediction via Web UI

1. Open http://localhost:30081
2. Enter patient data:
   - Age: 63
   - Sex: Male (1)
   - Chest Pain Type: 3
   - Resting Blood Pressure: 145
   - Cholesterol: 233
   - Fasting Blood Sugar: Yes (1)
   - Resting ECG: 0
   - Max Heart Rate: 150
   - Exercise Angina: No (0)
   - ST Depression: 2.3
   - Slope: 0
   - CA: 0
   - Thal: 1
3. Click "Predict"
4. Verify you get a prediction result

### Test 2: Make a Prediction via API

**Using PowerShell:**
```powershell
Invoke-WebRequest -Uri "http://localhost:30080/predict" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"age": 63, "sex": 1, "cp": 3, "trestbps": 145, "chol": 233, "fbs": 1, "restecg": 0, "thalach": 150, "exang": 0, "oldpeak": 2.3, "slope": 0, "ca": 0, "thal": 1}'
```

**Using cURL (Git Bash/Linux/Mac):**
```bash
curl -X POST http://localhost:30080/predict \
  -H "Content-Type: application/json" \
  -d '{"age": 63, "sex": 1, "cp": 3, "trestbps": 145, "chol": 233, "fbs": 1, "restecg": 0, "thalach": 150, "exang": 0, "oldpeak": 2.3, "slope": 0, "ca": 0, "thal": 1}'
```

**Expected Response:**
```json
{
  "prediction": 1,
  "prediction_label": "Heart Disease",
  "probability": 0.85
}
```

### Test 3: Verify Metrics in Grafana

1. Make 10-20 predictions using the Web UI or API
2. Open Grafana: http://localhost:30300
3. Navigate to "Heart Disease API Metrics" dashboard
4. Verify:
   - ✅ Request Rate shows activity
   - ✅ Total Requests counter increases
   - ✅ API Health Status shows "Up" (green)
   - ✅ Cumulative Requests graph shows upward trend

### Test 4: Check Prometheus Metrics

1. Open http://localhost:30090
2. Go to "Graph" tab
3. Query: `api_requests_total`
4. Click "Execute"
5. Verify the counter value matches your test requests

---

## Troubleshooting

### Issue 1: Pods Not Starting

**Check pod status:**
```bash
kubectl get pods
```

**View pod logs:**
```bash
# Replace <pod-name> with actual pod name
kubectl logs <pod-name>

# Example
kubectl logs heart-api-deployment-xxxxx
```

**Describe pod for events:**
```bash
kubectl describe pod <pod-name>
```

**Solution:**
- Wait 1-2 minutes for images to pull
- Check Docker Desktop is running
- Ensure Kubernetes is enabled in Docker Desktop

---

### Issue 2: Cannot Access Services

**Check services:**
```bash
kubectl get services
```

**Verify NodePorts:**
- heart-api-service: 30080
- heart-ui-service: 30081
- mlflow-service: 30050
- prometheus-service: 30090
- grafana-service: 30300

**Solution:**
- Restart Docker Desktop
- Delete and reapply deployments:
  ```bash
  kubectl delete -f k8s/
  kubectl apply -f k8s/
  ```

---

### Issue 3: Grafana Shows "No Data"

**Possible Causes:**
- No API requests made yet
- Prometheus not scraping metrics

**Solution:**
1. Make some predictions to generate traffic
2. Check Prometheus targets: http://localhost:30090/targets
3. Verify `heart-api` target is "UP"
4. Wait 10-15 seconds for metrics to appear

---

### Issue 4: MLflow UI Not Loading

**Check MLflow pod:**
```bash
kubectl get pods -l app=mlflow
```

**Restart MLflow:**
```bash
kubectl delete pod -l app=mlflow
```

**Alternative - Run MLflow Locally:**
```bash
mlflow ui
# Access at http://localhost:5000
```

---

### Issue 5: Model Not Found Error

**Symptom:** API returns "Model not found" error

**Solution:**
1. Run the ML pipeline first:
   ```bash
   python run_local_pipeline.py
   ```
2. Verify model exists:
   ```bash
   ls models/
   ls mlruns/
   ```
3. Rebuild Docker image:
   ```bash
   docker build -t heart-api .
   ```
4. Redeploy:
   ```bash
   kubectl delete -f k8s/deployment.yaml
   kubectl apply -f k8s/deployment.yaml
   ```

---

## Quick Reference - All Access URLs

| Service | URL | Credentials | Purpose |
|---------|-----|-------------|---------|
| **Web UI** | http://localhost:30081 | None | Make predictions via form |
| **API Docs** | http://localhost:30080/docs | None | Interactive API documentation |
| **API (ReDoc)** | http://localhost:30080/redoc | None | Alternative API docs |
| **MLflow** | http://localhost:30050 | None | Experiment tracking |
| **Prometheus** | http://localhost:30090 | None | Metrics collection |
| **Grafana** | http://localhost:30300 | admin/admin | Monitoring dashboards |

---

## Complete Workflow Summary

### For First-Time Setup:

1. **Clone repository** and install dependencies
2. **Run ML pipeline**: `python run_local_pipeline.py`
3. **View experiments**: `mlflow ui` → http://localhost:5000
4. **Build Docker images**: `docker build -t heart-api .` and `docker build -f Dockerfile.ui -t heart-ui .`
5. **Deploy to Kubernetes**: `kubectl apply -f k8s/`
6. **Wait for pods**: `kubectl get pods` (all should be Running)
7. **Access services**: Use URLs from Quick Reference table
8. **Test predictions**: Use Web UI or API
9. **Monitor metrics**: Check Grafana and Prometheus

### For Daily Development:

1. **Make code changes**
2. **Test locally**: `python run_local_pipeline.py`
3. **Rebuild images**: `docker build -t heart-api .`
4. **Update deployment**: `kubectl delete -f k8s/deployment.yaml && kubectl apply -f k8s/deployment.yaml`
5. **Verify changes**: Test via Web UI or API
6. **Monitor**: Check Grafana dashboard

---

## Additional Resources

- **Kubernetes Deployment Guide**: [docs/KUBERNETES_DEPLOYMENT.md](docs/KUBERNETES_DEPLOYMENT.md)
- **Grafana Dashboard Guide**: [docs/GRAFANA_DASHBOARD.md](docs/GRAFANA_DASHBOARD.md)
- **Prometheus Dashboard Guide**: [docs/PROMETHEUS_DASHBOARD.md](docs/PROMETHEUS_DASHBOARD.md)
- **API Documentation**: [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)
- **Configuration Guide**: [docs/CONFIGURATION_GUIDE.md](docs/CONFIGURATION_GUIDE.md)

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the documentation in the `docs/` folder
3. Check pod logs: `kubectl logs <pod-name>`
4. Verify all services are running: `kubectl get all`

---

**Happy Testing! 🚀**
