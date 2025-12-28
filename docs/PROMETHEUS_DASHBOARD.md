# Prometheus Monitoring Dashboard

## Overview
This document provides Prometheus queries and dashboard configuration for monitoring the Heart Disease MLOps application.

## Access Prometheus

Based on your Kubernetes services, Prometheus is accessible at:
- **URL**: `http://localhost:30090`
- **Service**: `prometheus-service` (NodePort 30090)

## Key Metrics Available

### 1. API Request Metrics

#### Total API Requests
```promql
api_requests_total
```

#### Request Rate (requests per second)
```promql
rate(api_requests_total[5m])
```

#### Request Rate by Endpoint
```promql
rate(api_requests_total[5m]) * 60
```

### 2. HTTP Metrics (if available)

#### HTTP Request Duration (95th percentile)
```promql
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

#### HTTP Request Rate by Status Code
```promql
sum(rate(http_requests_total[5m])) by (status)
```

#### Error Rate (4xx and 5xx responses)
```promql
sum(rate(http_requests_total{status=~"4..|5.."}[5m]))
```

### 3. Application Performance

#### Request Latency (average)
```promql
rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])
```

#### Requests per Minute
```promql
increase(api_requests_total[1m])
```

#### Successful Predictions Rate
```promql
rate(api_requests_total[5m]) - rate(http_requests_total{status=~"4..|5.."}[5m])
```

### 4. System Metrics

#### CPU Usage
```promql
rate(process_cpu_seconds_total[5m]) * 100
```

#### Memory Usage (bytes)
```promql
process_resident_memory_bytes
```

#### Memory Usage (MB)
```promql
process_resident_memory_bytes / 1024 / 1024
```

#### Open File Descriptors
```promql
process_open_fds
```

### 5. Python-Specific Metrics

#### Garbage Collection Count
```promql
rate(python_gc_collections_total[5m])
```

#### Python Info
```promql
python_info
```

## Dashboard Panels Configuration

### Panel 1: Request Rate Over Time
- **Query**: `rate(api_requests_total[5m])`
- **Type**: Graph
- **Description**: Shows the rate of API requests per second

### Panel 2: Total Requests Counter
- **Query**: `api_requests_total`
- **Type**: Stat/Single Stat
- **Description**: Total number of API requests since startup

### Panel 3: Memory Usage
- **Query**: `process_resident_memory_bytes / 1024 / 1024`
- **Type**: Graph
- **Description**: Memory usage in MB over time

### Panel 4: CPU Usage
- **Query**: `rate(process_cpu_seconds_total[5m]) * 100`
- **Type**: Graph
- **Description**: CPU usage percentage

### Panel 5: Request Latency
- **Query**: `rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])`
- **Type**: Graph
- **Description**: Average request latency in seconds

### Panel 6: Error Rate
- **Query**: `sum(rate(http_requests_total{status=~"4..|5.."}[5m]))`
- **Type**: Graph
- **Description**: Rate of error responses (4xx and 5xx)

## Creating a Dashboard in Prometheus

### Option 1: Using Prometheus UI

1. Open Prometheus at `http://localhost:30090`
2. Go to **Graph** tab
3. Enter any query from above
4. Click **Execute**
5. Switch to **Graph** view to see visualization

### Option 2: Using Grafana (Recommended)

For a better dashboard experience, use Grafana with Prometheus as a data source:

1. **Deploy Grafana** (if not already deployed)
2. **Add Prometheus as Data Source**:
   - URL: `http://prometheus-service:9090`
3. **Create Dashboard** with panels using the queries above

## Quick Monitoring Commands

### Check if metrics are being collected
```bash
curl http://localhost:30090/api/v1/query?query=api_requests_total
```

### Check current request rate
```bash
curl http://localhost:30090/api/v1/query?query=rate(api_requests_total[5m])
```

### Check memory usage
```bash
curl http://localhost:30090/api/v1/query?query=process_resident_memory_bytes
```

## Alerting Rules (Optional)

### High Error Rate Alert
```yaml
- alert: HighErrorRate
  expr: sum(rate(http_requests_total{status=~"5.."}[5m])) > 0.05
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "High error rate detected"
    description: "Error rate is above 5% for 5 minutes"
```

### High Memory Usage Alert
```yaml
- alert: HighMemoryUsage
  expr: process_resident_memory_bytes / 1024 / 1024 > 500
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "High memory usage"
    description: "Memory usage is above 500MB"
```

## Testing Metrics Collection

### Generate some API requests
```bash
# Make prediction requests to generate metrics
curl -X POST http://localhost:30080/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 54, "sex": 1, "cp": 0, "trestbps": 130,
    "chol": 246, "fbs": 0, "restecg": 1,
    "thalach": 150, "exang": 0, "oldpeak": 1.2,
    "slope": 2, "ca": 0, "thal": 2
  }'
```

### Check metrics endpoint
```bash
curl http://localhost:30080/metrics
```

## Useful Prometheus Expressions

### Top 5 Endpoints by Request Count
```promql
topk(5, api_requests_total)
```

### Request Rate Increase (last hour vs previous hour)
```promql
increase(api_requests_total[1h]) - increase(api_requests_total[1h] offset 1h)
```

### Prediction Throughput (predictions per minute)
```promql
rate(api_requests_total[1m]) * 60
```

## Dashboard JSON (for Grafana Import)

Save this as a `.json` file and import into Grafana:

```json
{
  "dashboard": {
    "title": "Heart Disease API Monitoring",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [{"expr": "rate(api_requests_total[5m])"}],
        "type": "graph"
      },
      {
        "title": "Total Requests",
        "targets": [{"expr": "api_requests_total"}],
        "type": "stat"
      },
      {
        "title": "Memory Usage (MB)",
        "targets": [{"expr": "process_resident_memory_bytes / 1024 / 1024"}],
        "type": "graph"
      },
      {
        "title": "CPU Usage (%)",
        "targets": [{"expr": "rate(process_cpu_seconds_total[5m]) * 100"}],
        "type": "graph"
      }
    ]
  }
}
```

## Next Steps

1. **Access Prometheus**: Open `http://localhost:30090` in your browser
2. **Run Queries**: Try the queries listed above in the Prometheus UI
3. **Generate Load**: Make some API requests to see metrics populate
4. **Optional**: Deploy Grafana for advanced dashboards
5. **Set Alerts**: Configure alerting rules for critical metrics
