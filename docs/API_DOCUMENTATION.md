# Heart Disease Prediction API Documentation

This API provides real-time predictions for heart disease risk based on clinical health data.

## Base URL
`http://localhost:8000` (Local Docker/Uvicorn)
`http://localhost:30080` (Kubernetes NodePort)

---

## Endpoints

### 1. Health Check
**GET** `/`

Checks if the API is running.

**Response:**
```json
{
  "status": "ok",
  "message": "Heart Disease Prediction API is running"
}
```

---

### 2. Predict Heart Disease
**POST** `/predict`

Predicts the presence of heart disease.

**Request Body (JSON):**

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `age` | float | Age in years | `63` |
| `sex` | float | 1 = male, 0 = female | `1` |
| `cp` | float | Chest pain type (0-3) | `3` |
| `trestbps` | float | Resting blood pressure (mm Hg) | `145` |
| `chol` | float | Serum cholestoral in mg/dl | `233` |
| `fbs` | float | Fasting blood sugar > 120 mg/dl (1 = true; 0 = false) | `1` |
| `restecg` | float | Resting electrocardiographic results (0-2) | `0` |
| `thalach` | float | Maximum heart rate achieved | `150` |
| `exang` | float | Exercise induced angina (1 = yes; 0 = no) | `0` |
| `oldpeak` | float | ST depression induced by exercise relative to rest | `2.3` |
| `slope` | float | Slope of the peak exercise ST segment (0-2) | `0` |
| `ca` | float | Number of major vessels (0-3) colored by flourosopy | `0` |
| `thal` | float | Thalassemia (1 = normal; 2 = fixed defect; 3 = reversable defect) | `1` |

**Example Payload:**
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

**Response (JSON):**

| Field | Type | Description |
|-------|------|-------------|
| `prediction` | int | 0 = No Disease, 1 = Disease |
| `confidence` | float | Probability of the positive class (Disease) |

**Example Response:**
```json
{
  "prediction": 1,
  "confidence": 0.85
}
```

---

### 3. Metrics
**GET** `/metrics`

Exposes Prometheus metrics.

**Response:**
Plain text format compatible with Prometheus scraping.
Example:
```text
# HELP api_requests_total Total API Requests Count
# TYPE api_requests_total counter
api_requests_total 5.0
...
```
