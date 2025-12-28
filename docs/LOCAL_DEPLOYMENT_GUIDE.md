# Complete Local Deployment Guide

This guide provides step-by-step instructions for running the Heart Disease MLOps project locally, including the pipeline, API, UI, and Prometheus monitoring.

## Prerequisites

Before starting, ensure you have the following installed:

- **Python 3.9+**
- **pip** (Python package manager)
- **Git** (optional, for cloning)

## 1. Setup and Installation

### 1.1 Clone or Download the Project

```bash
cd heart-disease-mlops-final
```

### 1.2 Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### 1.3 Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Running the Local Pipeline

The pipeline performs data acquisition, preprocessing, model training, experiment tracking, model packaging, and testing.

### 2.1 Run the Complete Pipeline

```bash
python run_local_pipeline.py
```

This will execute all 6 steps:
1. Data Acquisition
2. Preprocessing
3. Model Training
4. Experiment Tracking (MLflow)
5. Model Packaging
6. Unit Tests

**Expected Output:**
```
==================================================
Starting Local Heart Disease MLOps Pipeline
==================================================
[1/6] Running Data Acquisition...
[2/6] Running Preprocessing...
...
Pipeline Completed Successfully!
```

### 2.2 View MLflow Experiment Results

After running the pipeline, you can view experiment tracking results:

```bash
mlflow ui
```

Then open your browser to: **http://localhost:5000**

You'll see:
- All experiment runs
- Model metrics (accuracy, precision, recall, F1-score)
- Confusion matrices and ROC curves
- Model parameters

## 3. Running the API

The FastAPI application provides a REST API for heart disease predictions.

### 3.1 Start the API Server

```bash
uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
```

**Options:**
- `--reload`: Auto-reload on code changes (development mode)
- `--host 0.0.0.0`: Accept connections from any IP
- `--port 8000`: Run on port 8000

### 3.2 Access API Documentation

Open your browser to:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/

### 3.3 Test the API

**Using curl:**
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
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
     }'
```

**Using Python:**
```python
import requests

data = {
    "age": 63, "sex": 1, "cp": 3, "trestbps": 145,
    "chol": 233, "fbs": 1, "restecg": 0, "thalach": 150,
    "exang": 0, "oldpeak": 2.3, "slope": 0, "ca": 0, "thal": 1
}

response = requests.post("http://localhost:8000/predict", json=data)
print(response.json())
```

**Expected Response:**
```json
{
  "prediction": 1,
  "probability": 0.85,
  "model_version": "random_forest"
}
```

## 4. Running the UI

The UI provides a web interface for making predictions.

### 4.1 Serve the UI

The UI is a static HTML file. You can serve it using Python's built-in HTTP server:

```bash
cd ui
python -m http.server 8080
```

### 4.2 Access the UI

Open your browser to: **http://localhost:8080**

The UI allows you to:
- Input patient data via a form
- Submit predictions to the API
- View prediction results

**Note:** Make sure the API is running on port 8000 before using the UI.

## 5. Setting Up Prometheus Monitoring

Prometheus collects metrics from the API for monitoring and alerting.

### 5.1 Install Prometheus

**Windows:**
1. Download from: https://prometheus.io/download/
2. Extract to a folder (e.g., `C:\prometheus`)
3. Copy `monitoring/prometheus.yml` to the Prometheus folder

**Linux/Mac:**
```bash
# Using package manager (Ubuntu/Debian)
sudo apt-get install prometheus

# Or download binary
wget https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.linux-amd64.tar.gz
tar xvfz prometheus-*.tar.gz
cd prometheus-*
```

### 5.2 Configure Prometheus

The project includes a `monitoring/prometheus.yml` configuration file. Ensure it contains:

```yaml
scrape_configs:
  - job_name: 'heart-disease-api'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
```

### 5.3 Start Prometheus

**Windows:**
```bash
cd C:\prometheus
.\prometheus.exe --config.file=prometheus.yml
```

**Linux/Mac:**
```bash
./prometheus --config.file=monitoring/prometheus.yml
```

### 5.4 Access Prometheus UI

Open your browser to: **http://localhost:9090**

You can query metrics such as:
- `api_requests_total` - Total number of API requests
- `up` - Service availability

### 5.5 View API Metrics

The API exposes metrics at: **http://localhost:8000/metrics**

You'll see Prometheus-format metrics including:
```
# HELP api_requests_total Total API Requests Count
# TYPE api_requests_total counter
api_requests_total 42.0
```

## 6. Complete System Startup

To run the entire system locally:

### Terminal 1: Start the API
```bash
uvicorn src.app:app --host 0.0.0.0 --port 8000
```

### Terminal 2: Start the UI
```bash
cd ui
python -m http.server 8080
```

### Terminal 3: Start Prometheus
```bash
prometheus --config.file=monitoring/prometheus.yml
```

### Terminal 4: Start MLflow UI (Optional)
```bash
mlflow ui
```

### Access Points:
- **API**: http://localhost:8000/docs
- **UI**: http://localhost:8080
- **Prometheus**: http://localhost:9090
- **MLflow**: http://localhost:5000

## 7. Troubleshooting

### Issue: "No module named 'src'"
**Solution:** Ensure you're running commands from the project root directory.

### Issue: "Model not found"
**Solution:** Run the pipeline first to train and package the model:
```bash
python run_local_pipeline.py
```

### Issue: API returns 500 error
**Solution:** Check the API logs for errors. The model may not be loaded correctly.

### Issue: Prometheus shows "target down"
**Solution:** Ensure the API is running on port 8000 and accessible at http://localhost:8000/metrics

### Issue: UI cannot connect to API
**Solution:** 
1. Verify API is running: http://localhost:8000/docs
2. Check browser console for CORS errors
3. Ensure API has CORS enabled (already configured in `src/app.py`)

## 8. Stopping Services

To stop any running service, press `Ctrl+C` in the respective terminal.

To deactivate the virtual environment:
```bash
deactivate
```

## 9. Next Steps

- **Docker Deployment**: See `docs/KUBERNETES_DEPLOYMENT.md` for containerized deployment
- **Cloud Deployment**: Configure for AWS, GCP, or Azure
- **CI/CD**: Set up GitHub Actions workflows in `.github/workflows/`

## Summary

You now have a complete local MLOps environment running with:
- ✅ Trained ML models with experiment tracking
- ✅ REST API for predictions
- ✅ Web UI for user interaction
- ✅ Prometheus monitoring for observability
- ✅ MLflow for experiment management

For production deployment, refer to the Kubernetes deployment guide.
