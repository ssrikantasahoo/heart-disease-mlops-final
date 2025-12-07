import mlflow
import numpy as np
import pandas as pd

class HeartDiseaseInference:
    """
    Inference pipeline for loading MLflow model
    and generating predictions from incoming JSON.
    """

    def __init__(self, model_uri="runs:/<REPLACE_WITH_RUN_ID>/model"):
        """
        model_uri example:
        runs:/ab1234cdef/model
        Replace after first training run.
        """
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
    # Example test (replace run ID)
    sample = {
        "age": 54, "sex": 1, "cp": 0, "trestbps": 130,
        "chol": 246, "fbs": 0, "restecg": 1,
        "thalach": 150, "exang": 0, "oldpeak": 1.2,
        "slope": 2, "ca": 0, "thal": 2
    }

    inf = HeartDiseaseInference()
    print(inf.predict_single(sample))