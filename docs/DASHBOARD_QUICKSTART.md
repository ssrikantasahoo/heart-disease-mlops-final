# Prometheus Dashboard Quick Start

## Access Your Monitoring

Your Prometheus instance is already running! Access it at:
**http://localhost:30090**

## Quick Test Queries

Open Prometheus UI and try these queries:

### 1. Total API Requests
```
api_requests_total
```

### 2. Request Rate (last 5 minutes)
```
rate(api_requests_total[5m])
```

### 3. Memory Usage (MB)
```
process_resident_memory_bytes / 1024 / 1024
```

### 4. CPU Usage (%)
```
rate(process_cpu_seconds_total[5m]) * 100
```

## Generate Test Traffic

Run this command to generate some API requests:

```powershell
# Windows PowerShell
for ($i=1; $i -le 10; $i++) {
    curl.exe -X POST http://localhost:30080/predict `
      -H "Content-Type: application/json" `
      -d '{\"age\": 54, \"sex\": 1, \"cp\": 0, \"trestbps\": 130, \"chol\": 246, \"fbs\": 0, \"restecg\": 1, \"thalach\": 150, \"exang\": 0, \"oldpeak\": 1.2, \"slope\": 2, \"ca\": 0, \"thal\": 2}'
    Start-Sleep -Seconds 1
}
```

## View Metrics Endpoint

Check raw metrics:
```powershell
curl.exe http://localhost:30080/metrics
```

## Dashboard Panels

Your dashboard includes:
- ✅ API Request Rate (requests/second)
- ✅ Total Requests Counter
- ✅ Memory Usage (MB)
- ✅ CPU Usage (%)
- ✅ Requests per Minute

## Next Steps

1. **Open Prometheus**: http://localhost:30090
2. **Run test queries** from above
3. **Generate traffic** using the PowerShell script
4. **Watch metrics update** in real-time

For detailed queries and Grafana setup, see `PROMETHEUS_DASHBOARD.md`
