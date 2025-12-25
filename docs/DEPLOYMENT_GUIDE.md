# Local Kubernetes Deployment Guide

This guide details how to build, package, and deploy the Heart Disease Prediction API to a local Kubernetes cluster (Docker Desktop) and how to troubleshoot common issues.

## 1. Prerequisites

- **Docker Desktop** installed and running.
- **Kubernetes** enabled in Docker Desktop settings.
- **Python 3.9+** installed.
- **Dependencies** installed:
  ```bash
  pip install -r requirements.txt
  ```

## 2. Prepare the Model (Robust Packaging)

We use a specific packaging script to save the production model to a static directory (`models/production_model`). This avoids issues with dynamic MLflow run IDs in containers.

1. **Run the packaging script:**
   ```bash
   python src/model_packaging.py
   ```
   *Output:* verifying `Model saved successfully to models/production_model`.

## 3. Build the Docker Image

Build the image locally. We use `--no-cache` to ensure the latest model files are copied.

```bash
docker build --no-cache -t heart-api .
```

*Note: The Dockerfile is configured to COPY `models/` into the container.*

2. **Build the UI Image:**
   ```bash
   docker build -f Dockerfile.ui -t heart-ui .
   ```

## 4. Deploy to Kubernetes

We use `kubectl` to apply the manifests located in the `k8s/` directory.

1. **Apply Manifests:**
   ```bash
   kubectl apply -f k8s/
   ```
   This creates:
   - `Deployment`: Manages the API pods (replicas).
   - `Service`: Exposes the API on NodePort 30080.
   - `Ingress`: (Optional) Ingress rules.

2. **Verify Deployment:**
   ```bash
   kubectl get pods
   ```
   *Expected Status:* `Running` and `1/1` Ready.

3. **Check Services:**
   ```bash
   kubectl get services
   ```
   Ensure `heart-api-service` lists port `8000:30080`.

## 5. Test the API

Send a POST request to `http://localhost:30080/predict` with patient data.

**PowerShell Example:**
```powershell
Invoke-RestMethod -Method Post -Uri "http://localhost:30080/predict" -ContentType "application/json" -Body '{"age": 50, "sex": 1, "cp": 0, "trestbps": 130, "chol": 250, "fbs": 0, "restecg": 1, "thalach": 160, "exang": 0, "oldpeak": 1.0, "slope": 2, "ca": 0, "thal": 2}'
```

**Curl Example:**
```bash
curl -X POST "http://localhost:30080/predict" \
     -H "Content-Type: application/json" \
     -d '{"age": 50, "sex": 1, "cp": 0, "trestbps": 130, "chol": 250, "fbs": 0, "restecg": 1, "thalach": 160, "exang": 0, "oldpeak": 1.0, "slope": 2, "ca": 0, "thal": 2}'
```

## 6. Troubleshooting

**Issue: Pods in `CrashLoopBackOff`**
- **Cause**: Application failed to start, usually due to missing model files.
- **Fix**:
  1. Check logs: `kubectl logs <pod-name>`
  2. If "File not found", verify `src/model_packaging.py` was run RECENTLY.
  3. Rebuild image: `docker build --no-cache -t heart-api .`
  4. Restart pods: `kubectl rollout restart deployment/heart-api-deployment`

**Issue: `kubectl` connection refused**
- **Cause**: Kubernetes not enabled or context not selected.
- **Fix**: Enable Kubernetes in Docker Desktop settings and ensure context is `docker-desktop`.
