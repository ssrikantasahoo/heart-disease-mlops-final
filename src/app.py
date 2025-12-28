from fastapi import FastAPI, Request
from pydantic import BaseModel
import logging
import os
from prometheus_client import Counter, generate_latest
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware

from config import config
from inference_pipeline import HeartDiseaseInference
from experiment_tracking import run_experiment

# --------------------------
# Logging Setup
# --------------------------
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format=config.LOG_FORMAT
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
    title=config.API_TITLE,
    description=config.API_DESCRIPTION,
    version=config.API_VERSION
)

# --------------------------
# CORS Middleware
# --------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ALLOW_ORIGINS,
    allow_credentials=config.CORS_ALLOW_CREDENTIALS,
    allow_methods=config.CORS_ALLOW_METHODS,
    allow_headers=config.CORS_ALLOW_HEADERS,
)


# --------------------------
# MLflow model loader
# --------------------------
# Determine the absolute path to the project root (one level up from src/)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

import mlflow

# Path to the models directory for the specific experiment
# Dynamically resolve experiment ID by name
experiment_name = config.EXPERIMENT_NAME
mlflow.set_tracking_uri(config.MLFLOW_TRACKING_URI)
experiment = mlflow.get_experiment_by_name(experiment_name)

if experiment:
    experiment_id = experiment.experiment_id
    models_dir = os.path.join(project_root, "mlruns", experiment_id, "models")
else:
    # If experiment doesn't exist, we can't find models, so we'll treat it as empty
    experiment_id = None
    models_dir = ""

def get_latest_model_uri():
    """
    Finds the latest model artifact in the specified directory.
    """
    try:
        # Check if the directory exists
        if not os.path.exists(models_dir):
            logger.error(f"Models directory not found: {models_dir}")
            return None

        # Get all subdirectories in the models folder
        subdirs = [os.path.join(models_dir, d) for d in os.listdir(models_dir) 
                   if os.path.isdir(os.path.join(models_dir, d))]
        
        if not subdirs:
            logger.error(f"No model directories found in {models_dir}")
            return None

        # Sort by modification time (latest first)
        latest_model_dir = max(subdirs, key=os.path.getmtime)
        
        # Construct path to artifacts
        artifact_path = os.path.join(latest_model_dir, "artifacts")
        
        if os.name == 'nt':
            artifact_path = artifact_path.replace("\\", "/")
            
        return f"file:///{artifact_path}"

    except Exception as e:
        logger.error(f"Error finding latest model: {e}")
        return None

# Get dynamic model URI
dynamic_model_uri = get_latest_model_uri()

if not dynamic_model_uri:
    logger.info("No model found. Starting auto-train pipeline...")
    # This expects run_experiment to return the model_uri or we find it again
    # We rely on run_experiment returning the model URI now.
    dynamic_model_uri = run_experiment()
    logger.info(f"Auto-training completed. New Model URI: {dynamic_model_uri}")

# Fallback or Environment Override
MODEL_URI = os.getenv("MLFLOW_MODEL_URI", dynamic_model_uri)

if not MODEL_URI:
    raise RuntimeError("Could not determine MODEL_URI. Please set MLFLOW_MODEL_URI or ensure models exist in mlruns.")

logger.info(f"Using Model URI: {MODEL_URI}")
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
