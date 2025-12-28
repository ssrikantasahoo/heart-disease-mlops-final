"""
Centralized configuration module for Heart Disease MLOps project.

All configuration values can be overridden via environment variables.
This module provides defaults and loads from environment when available.
"""

import os
from typing import List


class Config:
    """Centralized configuration with environment variable support."""
    
    # ======================
    # Data Configuration
    # ======================
    DATA_URL: str = os.getenv(
        "DATA_URL",
        "https://archive.ics.uci.edu/static/public/45/heart+disease.zip"
    )
    DATA_DIR: str = os.getenv("DATA_DIR", "data")
    CSV_FILENAME: str = os.getenv("CSV_FILENAME", "heart.csv")
    TARGET_DATA_FILE: str = os.getenv("TARGET_DATA_FILE", "processed.cleveland.data")
    
    @property
    def CSV_PATH(self) -> str:
        """Full path to the CSV file."""
        return os.path.join(self.DATA_DIR, self.CSV_FILENAME)
    
    # ======================
    # Dataset Schema
    # ======================
    COLUMN_NAMES: List[str] = [
        'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
        'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target'
    ]
    
    CATEGORICAL_COLUMNS: List[str] = [
        'cp', 'restecg', 'slope', 'thal', 'sex', 'fbs', 'exang', 'ca'
    ]
    
    # ======================
    # MLflow Configuration
    # ======================
    EXPERIMENT_NAME: str = os.getenv("MLFLOW_EXPERIMENT_NAME", "heart-disease-experiment")
    MLRUNS_DIR: str = os.getenv("MLRUNS_DIR", "mlruns")
    
    @property
    def MLFLOW_TRACKING_URI(self) -> str:
        """MLflow tracking URI."""
        # Determine project root dynamically
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        return os.getenv(
            "MLFLOW_TRACKING_URI",
            f"file:///{os.path.join(project_root, self.MLRUNS_DIR)}"
        )
    
    # ======================
    # Model Configuration
    # ======================
    RANDOM_STATE: int = int(os.getenv("RANDOM_STATE", "42"))
    TEST_SIZE: float = float(os.getenv("TEST_SIZE", "0.2"))
    CV_FOLDS: int = int(os.getenv("CV_FOLDS", "5"))
    
    # Production model output path
    PRODUCTION_MODEL_DIR: str = os.getenv("PRODUCTION_MODEL_DIR", "models/production_model")
    
    # Logistic Regression hyperparameters
    LOGREG_MAX_ITER: int = int(os.getenv("LOGREG_MAX_ITER", "1000"))
    
    # Random Forest hyperparameters
    RF_N_ESTIMATORS: int = int(os.getenv("RF_N_ESTIMATORS", "200"))
    RF_MAX_DEPTH: int = int(os.getenv("RF_MAX_DEPTH", "6")) if os.getenv("RF_MAX_DEPTH") else None
    RF_MIN_SAMPLES_SPLIT: int = int(os.getenv("RF_MIN_SAMPLES_SPLIT", "5"))
    
    # GridSearch parameters for train.py
    GRID_N_ESTIMATORS: List[int] = [100, 200]
    GRID_MAX_DEPTH: List = [None, 6, 10]
    GRID_MIN_SAMPLES_SPLIT: List[int] = [2, 5]
    GRID_N_JOBS: int = int(os.getenv("GRID_N_JOBS", "-1"))
    
    # ======================
    # API Configuration
    # ======================
    API_TITLE: str = os.getenv("API_TITLE", "Heart Disease Prediction API")
    API_DESCRIPTION: str = os.getenv(
        "API_DESCRIPTION",
        "FastAPI service for predicting heart disease using MLflow model"
    )
    API_VERSION: str = os.getenv("API_VERSION", "1.0")
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    
    # CORS Configuration
    CORS_ALLOW_ORIGINS: List[str] = os.getenv(
        "CORS_ALLOW_ORIGINS",
        "*"
    ).split(",")
    CORS_ALLOW_CREDENTIALS: bool = os.getenv("CORS_ALLOW_CREDENTIALS", "true").lower() == "true"
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    # ======================
    # Logging Configuration
    # ======================
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "%(asctime)s — %(levelname)s — %(message)s")


# Create a singleton instance
config = Config()


# Convenience function for getting config
def get_config() -> Config:
    """Get the configuration instance."""
    return config


if __name__ == "__main__":
    # Display current configuration
    print("=== Heart Disease MLOps Configuration ===\n")
    
    print("[Data Configuration]")
    print(f"  DATA_URL: {config.DATA_URL}")
    print(f"  DATA_DIR: {config.DATA_DIR}")
    print(f"  CSV_PATH: {config.CSV_PATH}")
    print(f"  TARGET_DATA_FILE: {config.TARGET_DATA_FILE}")
    
    print("\n[MLflow Configuration]")
    print(f"  EXPERIMENT_NAME: {config.EXPERIMENT_NAME}")
    print(f"  MLFLOW_TRACKING_URI: {config.MLFLOW_TRACKING_URI}")
    
    print("\n[Model Configuration]")
    print(f"  RANDOM_STATE: {config.RANDOM_STATE}")
    print(f"  TEST_SIZE: {config.TEST_SIZE}")
    print(f"  CV_FOLDS: {config.CV_FOLDS}")
    print(f"  PRODUCTION_MODEL_DIR: {config.PRODUCTION_MODEL_DIR}")
    
    print("\n[Logistic Regression]")
    print(f"  MAX_ITER: {config.LOGREG_MAX_ITER}")
    
    print("\n[Random Forest]")
    print(f"  N_ESTIMATORS: {config.RF_N_ESTIMATORS}")
    print(f"  MAX_DEPTH: {config.RF_MAX_DEPTH}")
    print(f"  MIN_SAMPLES_SPLIT: {config.RF_MIN_SAMPLES_SPLIT}")
    
    print("\n[API Configuration]")
    print(f"  API_TITLE: {config.API_TITLE}")
    print(f"  API_VERSION: {config.API_VERSION}")
    print(f"  API_HOST: {config.API_HOST}")
    print(f"  API_PORT: {config.API_PORT}")
    print(f"  CORS_ALLOW_ORIGINS: {config.CORS_ALLOW_ORIGINS}")
    
    print("\n[Logging]")
    print(f"  LOG_LEVEL: {config.LOG_LEVEL}")
