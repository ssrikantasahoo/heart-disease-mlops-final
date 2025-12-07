from fastapi import FastAPI, Request
from pydantic import BaseModel
import logging
import os
from prometheus_client import Counter, generate_latest
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware

from inference_pipeline import HeartDiseaseInference

# --------------------------
# Logging Setup
# --------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)
logger = logging.getLogger("api_log")

# --------------------------
# Prometheus Metrics
# --------------------------
REQUEST_COUNT = Counter(
    "api_requests_total",
    "Total API Requests Count"
)

# --------------------------
# FastAPI App
# --------------------------
app = FastAPI(
    title="Heart Disease Prediction API",
    description="FastAPI service for predicting heart disease using MLflow model",
    version="1.0"
)

# --------------------------
# CORS Middleware
# --------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------
# MLflow model loader
# Replace <RUN_ID> after running MLflow training or set MLFLOW_MODEL_URI env var
# --------------------------
MODEL_URI = os.getenv(
    "MLFLOW_MODEL_URI",
    "file:///c:/Users/ssrik/Downloads/heart-disease-mlops-final/mlruns/782724371802594758/models/"
    "m-d2685904365445a585d9fa5f71e5a520/artifacts"
)
inference_engine = HeartDiseaseInference(model_uri=MODEL_URI)


# --------------------------
# Request Body Schema
# --------------------------
class PatientData(BaseModel):
    age: float
    sex: float
    cp: float
    trestbps: float
    chol: float
    fbs: float
    restecg: float
    thalach: float
    exang: float
    oldpeak: float
    slope: float
    ca: float
    thal: float


# --------------------------
# Prediction Endpoint
# --------------------------
@app.post("/predict")
async def predict(data: PatientData, request: Request):
    REQUEST_COUNT.inc()

    input_dict = data.dict()
    logger.info(f"Received request: {input_dict}")

    result = inference_engine.predict_single(input_dict)
    logger.info(f"Prediction: {result}")

    return result


# --------------------------
# Metrics Endpoint
# --------------------------
@app.get("/metrics", response_class=PlainTextResponse)
async def metrics():
    return generate_latest()


# --------------------------
# Health Check
# --------------------------
@app.get("/")
def health():
    return {"status": "ok", "message": "Heart Disease Prediction API is running"}
