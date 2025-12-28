# Kubernetes Deployment Guide

This guide provides comprehensive instructions for deploying the Heart Disease MLOps project to Kubernetes, including how to work with MLflow models.

## Prerequisites

- **Docker Desktop** installed and running
- **Kubernetes** enabled in Docker Desktop (Settings → Kubernetes → Enable Kubernetes)
- **kubectl** CLI installed (comes with Docker Desktop)
- **Python 3.9+** installed locally (for initial model training)
- Project files downloaded/cloned

## 1. Train the Model First (Important!)

Before deploying to Kubernetes, train the model locally to ensure model artifacts exist.

### 1.1 Install Dependencies Locally

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 1.2 Run the Training Pipeline

```bash
python run_local_pipeline.py
```

This trains the models and saves them to the `mlruns/` directory.

### 1.3 Verify Models Exist

```bash
# Windows:
dir mlruns\782724371802594758\models\

# Linux/Mac:
ls mlruns/782724371802594758/models/
```

You should see model directories like `m-abc123...`.

## 2. Build Docker Images

Kubernetes needs Docker images to deploy. Build them locally for Docker Desktop Kubernetes.

### 2.1 Build the API Image

```bash
docker build -t heart-api:latest -f Dockerfile .
```

### 2.2 Build the UI Image

```bash
docker build -t heart-ui:latest -f Dockerfile.ui .
```

### 2.3 Verify Images

```bash
docker images --filter "reference=heart*"
```

Expected output:
```
heart-api    latest    abc123...    2 minutes ago    500MB
heart-ui     latest    def456...    1 minute ago     25MB
```

> **Note:** The K8s manifests use `imagePullPolicy: Never` which tells Kubernetes to use local images instead of pulling from a registry.

## 3. Deploy to Kubernetes

### 3.1 Verify Kubernetes is Running

```bash
kubectl cluster-info
```

Expected output should show Kubernetes master running.

### 3.2 Apply Kubernetes Manifests

Deploy all resources at once:

```bash
kubectl apply -f k8s/
```

This creates:
- **Deployment** (`heart-api-deployment`) - Manages API pods
- **Service** (`heart-api-service`) - Exposes API on NodePort 30080
- **UI Deployment** (`heart-ui-deployment`) - Manages UI pods
- **UI Service** (`heart-ui-service`) - Exposes UI on NodePort 30081
- **Ingress** (optional) - Routes traffic based on hostname

### 3.3 Verify Deployment

**Check Pods:**
```bash
kubectl get pods
```

Expected output:
```
NAME                                   READY   STATUS    RESTARTS   AGE
heart-api-deployment-abc123-xyz        1/1     Running   0          30s
heart-ui-deployment-def456-uvw         1/1     Running   0          30s
```

**Check Services:**
```bash
kubectl get services
```

Expected output:
```
NAME                TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
heart-api-service   NodePort    10.96.100.50    <none>        8000:30080/TCP   1m
heart-ui-service    NodePort    10.96.100.51    <none>        80:30081/TCP     1m
```

**Check Deployments:**
```bash
kubectl get deployments
```

## 4. Access the Application

### 4.1 Understanding Kubernetes Services

The services were created when you ran `kubectl apply -f k8s/`. They expose your pods to the network.

**Check your services:**
```bash
kubectl get services
```

Expected output:
```
NAME                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
heart-api-service    NodePort    10.96.100.50     <none>        8000:30080/TCP   5m
heart-ui-service     NodePort    10.96.100.51     <none>        80:30081/TCP     5m
mlflow-service       NodePort    10.96.100.52     <none>        5000:30050/TCP   5m
prometheus-service   NodePort    10.96.100.53     <none>        9090:30090/TCP   5m
```

The format `8000:30080` means:
- **8000** = Internal cluster port
- **30080** = External NodePort (what you use to access from your machine)

### 4.2 Access Points

Based on the NodePort configuration in the K8s service manifests:

- **API Documentation**: http://localhost:30080/docs
- **API Health Check**: http://localhost:30080/
- **Web UI**: http://localhost:30081/
- **Metrics**: http://localhost:30080/metrics
- **Prometheus**: http://localhost:30090/
- **MLflow UI**: http://localhost:30050/

### 4.3 Verify Services are Running

**Test API health:**
```bash
curl http://localhost:30080/
```

Expected response:
```json
{
  "status": "ok",
  "message": "Heart Disease Prediction API is running"
}
```

**Open in browser:**
- API Swagger UI: http://localhost:30080/docs
- Web UI: http://localhost:30081/

### 4.4 Test the API

```bash
curl -X POST "http://localhost:30080/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 63, "sex": 1, "cp": 3, "trestbps": 145,
    "chol": 233, "fbs": 1, "restecg": 0, "thalach": 150,
    "exang": 0, "oldpeak": 2.3, "slope": 0, "ca": 0, "thal": 1
  }'
```

## 5. Working with MLflow Models in Kubernetes

### 5.1 Understanding Model Storage

The application automatically:
1. Looks for experiment named `"heart-disease-experiment"`
2. Finds the latest model in the `mlruns/` directory (copied into the container)
3. If no model exists, triggers auto-training on startup

### 5.2 View Logs (Including Auto-Training)

```bash
# Get pod name
kubectl get pods

# View logs
kubectl logs heart-api-deployment-abc123-xyz

# Follow logs in real-time
kubectl logs -f heart-api-deployment-abc123-xyz
```

If auto-training occurs, you'll see training progress in the logs.

### 5.3 Accessing MLflow UI from Kubernetes

**Option 1: Port Forward**
```bash
# Get pod name
kubectl get pods

# Port forward MLflow UI
kubectl exec -it heart-api-deployment-abc123-xyz -- mlflow ui --host 0.0.0.0 --port 5000 &
kubectl port-forward heart-api-deployment-abc123-xyz 5000:5000
```

Access: http://localhost:5000

**Option 2: Deploy MLflow as Separate Service**
Create `k8s/mlflow-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mlflow-ui
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mlflow-ui
  template:
    metadata:
      labels:
        app: mlflow-ui
    spec:
      containers:
      - name: mlflow
        image: heart-api:latest
        command: ["mlflow", "ui", "--host", "0.0.0.0", "--port", "5000"]
        ports:
        - containerPort: 5000
---
apiVersion: v1
kind: Service
metadata:
  name: mlflow-service
spec:
  type: NodePort
  selector:
    app: mlflow-ui
  ports:
  - port: 5000
    targetPort: 5000
    nodePort: 30050
```

Apply: `kubectl apply -f k8s/mlflow-deployment.yaml`
Access: http://localhost:30050

### 5.4 Updating Models

**Option 1: Rebuild and Redeploy**
```bash
# Train new model locally
python run_local_pipeline.py

# Rebuild image with new models
docker build -t heart-api:latest -f Dockerfile .

# Restart deployment to use new image
kubectl rollout restart deployment/heart-api-deployment
```

**Option 2: Use Persistent Volumes (Recommended for Production)**

Create `k8s/persistent-volume.yaml`:

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: mlruns-pv
spec:
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /path/to/mlruns
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mlruns-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
```

Update `k8s/deployment.yaml` to use the volume:

```yaml
spec:
  template:
    spec:
      containers:
      - name: heart-api
        volumeMounts:
        - name: mlruns-storage
          mountPath: /app/mlruns
      volumes:
      - name: mlruns-storage
        persistentVolumeClaim:
          claimName: mlruns-pvc
```

## 6. Scaling and Management

### 6.1 Scale the Deployment

```bash
# Scale to 3 replicas
kubectl scale deployment/heart-api-deployment --replicas=3

# Verify
kubectl get pods
```

### 6.2 Update Deployment

```bash
# After rebuilding image
kubectl rollout restart deployment/heart-api-deployment

# Check rollout status
kubectl rollout status deployment/heart-api-deployment
```

### 6.3 View Resource Usage

```bash
kubectl top pods
kubectl top nodes
```

## 7. Monitoring with Prometheus

### 7.1 Deploy Prometheus

Apply the monitoring manifest:

```bash
kubectl apply -f k8s/monitoring.yaml
```

### 7.2 Access Prometheus

```bash
kubectl port-forward service/prometheus-service 9090:9090
```

Access: http://localhost:9090

### 7.3 Query Metrics

In Prometheus UI, query:
- `api_requests_total` - Total API requests
- `up{job="heart-api"}` - Service health

## 8. Troubleshooting

### Issue: Pods in `CrashLoopBackOff`

**Check logs:**
```bash
kubectl logs heart-api-deployment-abc123-xyz
```

**Common causes:**
- Model not found (auto-training will trigger)
- Port conflict
- Resource limits exceeded

**Solution:**
```bash
# Describe pod for detailed info
kubectl describe pod heart-api-deployment-abc123-xyz

# Delete and recreate
kubectl delete pod heart-api-deployment-abc123-xyz
```

### Issue: `ImagePullBackOff`

**Cause:** Kubernetes trying to pull image from registry.

**Solution:** Verify `imagePullPolicy: Never` in `k8s/deployment.yaml`

### Issue: Cannot access via NodePort

**Check service:**
```bash
kubectl get svc heart-api-service
```

**Verify port mapping:**
```bash
kubectl describe svc heart-api-service
```

**Test from within cluster:**
```bash
kubectl run test-pod --image=curlimages/curl --rm -it -- curl http://heart-api-service:8000/
```

### Issue: Models not persisting across pod restarts

**Solution:** Use Persistent Volumes (see section 5.4)

## 9. Cleanup

### 9.1 Delete All Resources

```bash
kubectl delete -f k8s/
```

### 9.2 Verify Cleanup

```bash
kubectl get all
```

## 10. Production Considerations

### 10.1 Use Container Registry

For production, push images to a registry:

```bash
# Tag image
docker tag heart-api:latest your-registry.com/heart-api:v1.0

# Push to registry
docker push your-registry.com/heart-api:v1.0

# Update deployment.yaml
# image: your-registry.com/heart-api:v1.0
# imagePullPolicy: Always
```

### 10.2 Resource Limits

Add resource limits to `k8s/deployment.yaml`:

```yaml
resources:
  requests:
    memory: "512Mi"
    cpu: "500m"
  limits:
    memory: "1Gi"
    cpu: "1000m"
```

### 10.3 Health Checks

Already configured in `k8s/deployment.yaml`:
- **Liveness Probe** - Restarts pod if unhealthy
- **Readiness Probe** - Removes pod from service if not ready

### 10.4 Secrets Management

For sensitive data (API keys, credentials):

```bash
kubectl create secret generic mlflow-secrets \
  --from-literal=tracking-uri=your-tracking-uri

# Reference in deployment
env:
  - name: MLFLOW_TRACKING_URI
    valueFrom:
      secretKeyRef:
        name: mlflow-secrets
        key: tracking-uri
```

## 11. Summary

You now know how to:
- ✅ Train models locally before deployment
- ✅ Build Docker images for Kubernetes
- ✅ Deploy to Kubernetes cluster
- ✅ Work with MLflow models in K8s
- ✅ Scale and manage deployments
- ✅ Monitor with Prometheus
- ✅ Troubleshoot common issues

For local development without Kubernetes, see `docs/LOCAL_DEPLOYMENT_GUIDE.md`.
