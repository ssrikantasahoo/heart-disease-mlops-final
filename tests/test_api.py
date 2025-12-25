from fastapi.testclient import TestClient
from unittest.mock import patch
import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Mock the inference engine BEFORE importing app
with patch('inference_pipeline.HeartDiseaseInference') as MockEngine:
    mock_instance = MockEngine.return_value
    mock_instance.predict_single.return_value = {"prediction": 1, "confidence": 0.85}

    from app import app  # noqa: E402
    client = TestClient(app)


def test_predict_endpoint():
    payload = {
        "age": 50, "sex": 1, "cp": 0, "trestbps": 130,
        "chol": 250, "fbs": 0, "restecg": 1,
        "thalach": 160, "exang": 0, "oldpeak": 1.0,
        "slope": 2, "ca": 0, "thal": 2
    }

    response = client.post("/predict", json=payload)
    assert response.status_code == 200

    result = response.json()
    assert "prediction" in result
    assert "confidence" in result
    assert result["prediction"] == 1
    assert result["confidence"] == 0.85


def test_prediction_response_schema():
    payload = {
        "age": 50, "sex": 1, "cp": 0, "trestbps": 130,
        "chol": 250, "fbs": 0, "restecg": 1,
        "thalach": 160, "exang": 0, "oldpeak": 1.0,
        "slope": 2, "ca": 0, "thal": 2
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert "confidence" in response.json()

