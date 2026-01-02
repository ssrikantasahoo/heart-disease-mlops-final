# Grafana Dashboard Guide

This guide covers accessing and using Grafana for monitoring the Heart Disease MLOps API.

---

## 📊 Overview

Grafana provides rich visualization dashboards for monitoring your Heart Disease API metrics collected by Prometheus. The deployment includes:

- **Pre-configured Prometheus datasource** - Automatically connected to your Prometheus instance
- **Heart Disease API Metrics dashboard** - Ready-to-use dashboard with key performance indicators
- **Auto-provisioning** - Dashboards and datasources are automatically configured on startup

---

## 🚀 Accessing Grafana

### URL
**http://localhost:30300**

### Default Credentials
- **Username**: `admin`
- **Password**: `admin`

> [!IMPORTANT]
> On first login, Grafana will prompt you to change the default password. You can skip this for local development, but it's recommended to change it for production deployments.

---

## 📈 Pre-configured Dashboard

### Heart Disease API Metrics Dashboard

The dashboard includes the following panels:

#### 1. **API Request Rate**
- **Type**: Time series graph
- **Metric**: `rate(http_requests_total[1m])`
- **Description**: Shows the rate of incoming API requests per second
- **Use Case**: Monitor traffic patterns and detect unusual spikes

#### 2. **API Latency (P95)**
- **Type**: Gauge
- **Metric**: `http_request_duration_seconds{quantile="0.95"} * 1000`
- **Description**: 95th percentile response time in milliseconds
- **Thresholds**: 
  - Green: < 100ms
  - Yellow: 100-500ms
  - Red: > 500ms
- **Use Case**: Identify performance degradation

#### 3. **Predictions by Outcome**
- **Type**: Pie chart
- **Metric**: `sum by (prediction) (prediction_counter_total)`
- **Description**: Distribution of predictions (heart disease vs. no heart disease)
- **Use Case**: Understand prediction patterns and model behavior

#### 4. **HTTP Status Codes**
- **Type**: Bar chart
- **Metric**: `sum by (status_code) (http_requests_total)`
- **Description**: Distribution of HTTP response codes (200, 404, 500, etc.)
- **Use Case**: Monitor API health and error rates

#### 5. **API Health Status**
- **Type**: Status indicator
- **Metric**: `up{job="heart-api"}`
- **Description**: Shows if the API is up (green) or down (red)
- **Use Case**: Quick health check

#### 6. **Total Predictions**
- **Type**: Stat panel
- **Metric**: `sum(prediction_counter_total)`
- **Description**: Cumulative count of all predictions made
- **Use Case**: Track overall usage

#### 7. **Total HTTP Requests**
- **Type**: Stat panel
- **Metric**: `sum(http_requests_total)`
- **Description**: Total number of HTTP requests received
- **Use Case**: Monitor overall API usage

#### 8. **Average Latency (P50)**
- **Type**: Stat panel
- **Metric**: `http_request_duration_seconds{quantile="0.5"} * 1000`
- **Description**: Median response time in milliseconds
- **Use Case**: Monitor typical response times

---

## 🔧 Accessing the Dashboard

1. **Login to Grafana**
   - Navigate to http://localhost:30300
   - Enter credentials (admin/admin)
   - Skip or change password as prompted

2. **Open the Dashboard**
   - Click on **Dashboards** (four squares icon) in the left sidebar
   - Click **Browse**
   - Select **Heart Disease API Metrics**

3. **Refresh Settings**
   - The dashboard auto-refreshes every **5 seconds**
   - Time range is set to **Last 15 minutes**
   - You can adjust these in the top-right corner

---

## 🧪 Generating Test Data

To populate the dashboard with metrics, you need to generate API traffic:

### Using cURL

```bash
# Make a prediction request
curl -X POST http://localhost:30080/predict \
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

### Using the Web UI

1. Open http://localhost:30081
2. Fill in the patient data form
3. Click "Predict"
4. Repeat several times to generate traffic

### Using a Load Testing Script

```bash
# Run multiple requests
for i in {1..20}; do
  curl -X POST http://localhost:30080/predict \
    -H "Content-Type: application/json" \
    -d '{"age": 63, "sex": 1, "cp": 3, "trestbps": 145, "chol": 233, "fbs": 1, "restecg": 0, "thalach": 150, "exang": 0, "oldpeak": 2.3, "slope": 0, "ca": 0, "thal": 1}' \
    -s -o /dev/null
  echo "Request $i completed"
  sleep 1
done
```

After generating traffic, refresh the Grafana dashboard to see the metrics populate.

---

## 🎨 Creating Custom Dashboards

### Adding a New Panel

1. **Open Dashboard**
   - Navigate to the Heart Disease API Metrics dashboard
   - Click the **Add panel** button (top-right)

2. **Configure Panel**
   - Select **Add a new panel**
   - Choose visualization type (Graph, Gauge, Stat, etc.)
   - Enter your Prometheus query in the **Metrics** field

3. **Example Custom Queries**
   ```promql
   # Average request duration
   avg(http_request_duration_seconds)
   
   # Error rate (4xx and 5xx responses)
   sum(rate(http_requests_total{status_code=~"4..|5.."}[5m]))
   
   # Prediction rate by outcome
   rate(prediction_counter_total{prediction="heart_disease"}[1m])
   ```

4. **Save Panel**
   - Configure panel title and description
   - Click **Apply**
   - Click **Save dashboard** (disk icon, top-right)

### Creating a New Dashboard

1. Click **Dashboards** → **New Dashboard**
2. Click **Add a new panel**
3. Configure your panels as needed
4. Save with a descriptive name

---

## 🔍 Troubleshooting

### Dashboard Shows "No Data"

**Possible Causes:**
1. API hasn't received any requests yet
2. Prometheus isn't scraping metrics
3. Datasource isn't configured correctly

**Solutions:**
1. **Generate test traffic** (see section above)
2. **Check Prometheus**:
   ```bash
   # Verify Prometheus is running
   kubectl get pods -l app=prometheus
   
   # Access Prometheus UI
   # http://localhost:30090
   # Go to Status → Targets
   # Verify heart-api target is "UP"
   ```
3. **Verify Datasource**:
   - Go to Configuration → Data Sources
   - Click on "Prometheus"
   - Click "Test" button
   - Should show "Data source is working"

### Grafana Pod Not Starting

```bash
# Check pod status
kubectl get pods -l app=grafana

# View pod logs
kubectl logs -l app=grafana

# Describe pod for events
kubectl describe pod -l app=grafana
```

### Can't Access Grafana UI

**Check Service:**
```bash
# Verify service is running
kubectl get svc grafana-service

# Should show NodePort 30300
```

**Check Port Forwarding (Alternative):**
```bash
# If NodePort doesn't work, try port forwarding
kubectl port-forward svc/grafana-service 3000:3000

# Access at http://localhost:3000
```

### Forgot Admin Password

```bash
# Delete Grafana pod to reset (uses emptyDir, so data is lost)
kubectl delete pod -l app=grafana

# Wait for new pod to start
kubectl get pods -l app=grafana

# Login with admin/admin again
```

---

## 📊 Best Practices

### 1. **Set Up Alerts**
- Configure Grafana alerts for critical metrics
- Example: Alert when API latency > 500ms for 5 minutes
- Example: Alert when error rate > 5%

### 2. **Use Variables**
- Create dashboard variables for dynamic filtering
- Example: Filter by time range, environment, or service

### 3. **Organize Dashboards**
- Group related panels together
- Use rows to organize panels by category
- Add descriptive panel titles and descriptions

### 4. **Monitor Trends**
- Use longer time ranges to identify trends
- Compare current metrics to historical data
- Set up baseline alerts for anomaly detection

### 5. **Export Dashboards**
- Export dashboard JSON for backup
- Share dashboards with team members
- Version control dashboard configurations

---

## 🔗 Additional Resources

- **Grafana Documentation**: https://grafana.com/docs/
- **Prometheus Query Language**: https://prometheus.io/docs/prometheus/latest/querying/basics/
- **Dashboard Best Practices**: https://grafana.com/docs/grafana/latest/best-practices/

---

## 📝 Dashboard Configuration

The dashboard is automatically provisioned via Kubernetes ConfigMaps:

- **Datasource**: `grafana-datasources` ConfigMap
- **Dashboard Provider**: `grafana-dashboards-config` ConfigMap
- **Dashboard JSON**: `grafana-dashboard-heart-api` ConfigMap

To modify the dashboard:
1. Edit the ConfigMap in `k8s/grafana.yaml`
2. Apply changes: `kubectl apply -f k8s/grafana.yaml`
3. Restart Grafana: `kubectl delete pod -l app=grafana`

---

**Need help?** Check the [Prometheus Dashboard Guide](PROMETHEUS_DASHBOARD.md) for additional monitoring information.
