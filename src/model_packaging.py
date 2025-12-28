import mlflow
import mlflow.sklearn
import pandas as pd
import shutil
import os
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from config import config
from preprocessing import clean_dataset


def save_final_model():
    """Trains final model and saves it to a static directory 'models/production_model' for easy containerization."""
    # 1. Train Model
    print("Training production model...")
    df = pd.read_csv(config.CSV_PATH)
    df = clean_dataset(df)

    X = df.drop("target", axis=1)
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=config.TEST_SIZE, random_state=config.RANDOM_STATE
    )

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", RandomForestClassifier(
            n_estimators=100,  # Using tuned params
            max_depth=None,
            min_samples_split=config.RF_MIN_SAMPLES_SPLIT,
            random_state=config.RANDOM_STATE
        ))
    ])

    model.fit(X_train, y_train)

    # 2. Save using standard MLflow format but to a fixed path
    output_path = config.PRODUCTION_MODEL_DIR
    # Clean up existing
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    print(f"Saving model to {output_path}...")
    mlflow.sklearn.save_model(model, output_path)

    print(f"Model saved successfully to {output_path}")
    print("This directory can now be copied into Docker image.")


if __name__ == "__main__":
    save_final_model()
