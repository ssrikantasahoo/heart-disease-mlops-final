import mlflow
import pandas as pd
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_latest_model_uri():
    """
    Finds the latest model artifact in the mlruns directory.
    Returns the model URI or None if not found.
    """
    try:
        # Determine project root (one level up from src/)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        
        # Set MLflow tracking URI
        mlflow.set_tracking_uri(f"file:///{os.path.join(project_root, 'mlruns')}")
        
        # Get experiment by name
        experiment_name = "heart-disease-experiment"
        experiment = mlflow.get_experiment_by_name(experiment_name)
        
        if not experiment:
            logger.warning(f"Experiment '{experiment_name}' not found")
            return None
            
        experiment_id = experiment.experiment_id
        models_dir = os.path.join(project_root, "mlruns", experiment_id, "models")
        
        # Check if models directory exists
        if not os.path.exists(models_dir):
            logger.warning(f"Models directory not found: {models_dir}")
            return None
        
        # Get all subdirectories in the models folder
        subdirs = [
            os.path.join(models_dir, d) 
            for d in os.listdir(models_dir) 
            if os.path.isdir(os.path.join(models_dir, d))
        ]
        
        if not subdirs:
            logger.warning(f"No model directories found in {models_dir}")
            return None
        
        # Sort by modification time (latest first)
        latest_model_dir = max(subdirs, key=os.path.getmtime)
        
        # Construct path to artifacts
        artifact_path = os.path.join(latest_model_dir, "artifacts")
        
        if os.name == 'nt':  # Windows
            artifact_path = artifact_path.replace("\\", "/")
            
        model_uri = f"file:///{artifact_path}"
        logger.info(f"Found latest model: {model_uri}")
        return model_uri
        
    except Exception as e:
        logger.error(f"Error finding latest model: {e}")
        return None


class HeartDiseaseInference:
    """
    Inference pipeline for loading MLflow model
    and generating predictions from incoming JSON.
    """

    def __init__(self, model_uri=None):
        """
        Initialize inference pipeline with MLflow model.
        
        Args:
            model_uri: URI to the MLflow model. If None, will try to load from:
                      1. Latest model from mlruns directory (dynamic discovery)
                      2. MLFLOW_MODEL_URI environment variable
        
        Examples:
            - runs:/ab1234cdef/model
            - file:///path/to/mlruns/0/run_id/artifacts/model
        """
        if model_uri is None:
            # Try to find latest model dynamically
            logger.info("No model_uri provided, attempting dynamic discovery...")
            model_uri = get_latest_model_uri()
            
        if model_uri is None:
            # Fallback to environment variable
            logger.info("Dynamic discovery failed, checking MLFLOW_MODEL_URI environment variable...")
            model_uri = os.getenv("MLFLOW_MODEL_URI")
            
        if model_uri is None:
            raise ValueError(
                "Could not determine model URI. Please either:\n"
                "  1. Train a model first (run experiment_tracking.py)\n"
                "  2. Set MLFLOW_MODEL_URI environment variable\n"
                "  3. Provide model_uri as argument"
            )
        
        logger.info(f"Loading model from: {model_uri}")
        self.model = mlflow.sklearn.load_model(model_uri)

    def predict_single(self, input_dict: dict):
        """
        Predicts risk of heart disease for a single JSON input.
        Returns prediction + probability (confidence).
        """
        df = pd.DataFrame([input_dict])  # single-row dataframe

        # Model pipeline handles scaling + encoding
        pred = self.model.predict(df)[0]

        # Probability
        if hasattr(self.model, "predict_proba"):
            prob = self.model.predict_proba(df)[0][1]
        else:
            prob = float("nan")

        return {
            "prediction": int(pred),
            "confidence": float(prob)
        }


if __name__ == "__main__":
    # Example test - values can be overridden via environment variables
    # Default sample provided for quick testing
    sample = {
        "age": float(os.getenv("TEST_AGE", "54")),
        "sex": float(os.getenv("TEST_SEX", "1")),
        "cp": float(os.getenv("TEST_CP", "0")),
        "trestbps": float(os.getenv("TEST_TRESTBPS", "130")),
        "chol": float(os.getenv("TEST_CHOL", "246")),
        "fbs": float(os.getenv("TEST_FBS", "0")),
        "restecg": float(os.getenv("TEST_RESTECG", "1")),
        "thalach": float(os.getenv("TEST_THALACH", "150")),
        "exang": float(os.getenv("TEST_EXANG", "0")),
        "oldpeak": float(os.getenv("TEST_OLDPEAK", "1.2")),
        "slope": float(os.getenv("TEST_SLOPE", "2")),
        "ca": float(os.getenv("TEST_CA", "0")),
        "thal": float(os.getenv("TEST_THAL", "2"))
    }

    print("Testing inference pipeline with sample data:")
    print(f"Sample input: {sample}")
    
    try:
        inf = HeartDiseaseInference()
        result = inf.predict_single(sample)
        print(f"Prediction result: {result}")
    except ValueError as e:
        print(f"Error: {e}")
        print("Please set MLFLOW_MODEL_URI environment variable or provide model_uri argument.")

