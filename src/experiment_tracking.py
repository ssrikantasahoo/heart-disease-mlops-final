import mlflow
import mlflow.sklearn
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from config import config
from preprocessing import clean_dataset
from model_utils import get_model_metrics


def run_experiment():
    """
    Runs an MLflow experiment training both Logistic Regression and Random Forest on the cleaned Heart Disease dataset.
    Logs:
    - Parameters
    - Metrics
    - Models
    - Artifacts (comparison CSV)
    """

    # Load dataset
    df = pd.read_csv(config.CSV_PATH)
    df = clean_dataset(df)

    X = df.drop("target", axis=1)
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=config.TEST_SIZE, random_state=config.RANDOM_STATE
    )

    # ==========================================================
    # MLflow experiment
    # ==========================================================
    import os
    # Determine the absolute path to the project root (one level up from src/) since this file is in src/
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    mlflow.set_tracking_uri(config.MLFLOW_TRACKING_URI)
    mlflow.set_experiment(config.EXPERIMENT_NAME)

    # Helper to log plots
    import matplotlib.pyplot as plt
    from sklearn.metrics import ConfusionMatrixDisplay, RocCurveDisplay

    def log_plots(model, X_test, y_test, model_name):
        # Confusion Matrix
        plt.figure(figsize=(6, 6))
        ConfusionMatrixDisplay.from_estimator(model, X_test, y_test, cmap='Blues')
        plt.title(f"Confusion Matrix: {model_name}")
        cm_path = f"{model_name}_confusion_matrix.png"
        plt.savefig(cm_path)
        mlflow.log_artifact(cm_path)
        plt.close()

        # ROC Curve
        plt.figure(figsize=(6, 6))
        RocCurveDisplay.from_estimator(model, X_test, y_test)
        plt.title(f"ROC Curve: {model_name}")
        roc_path = f"{model_name}_roc_curve.png"
        plt.savefig(roc_path)
        mlflow.log_artifact(roc_path)
        plt.close()

    # ----- 1. Logistic Regression -----
    with mlflow.start_run(run_name="logistic_regression_run"):
        log_reg = Pipeline([
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=config.LOGREG_MAX_ITER))
        ])
        log_reg.fit(X_train, y_train)

        metrics = get_model_metrics(log_reg, X_test, y_test)

        # Log parameters
        mlflow.log_params({
            "model": "Logistic Regression",
            "scaler": "StandardScaler",
            "max_iter": 1000
        })

        # Log metrics
        mlflow.log_metrics(metrics)

        # Log plots
        log_plots(log_reg, X_test, y_test, "logistic_regression")

        # Log model
        mlflow.sklearn.log_model(log_reg, "logistic_regression")
        print(f"Logistic Regression Run ID: {mlflow.active_run().info.run_id}")
        print(f"Artifact URI: {mlflow.get_artifact_uri()}")

    # ----- 2. Random Forest -----
    with mlflow.start_run(run_name="random_forest_run"):
        rf = Pipeline([
            ("scaler", StandardScaler()),
            ("clf", RandomForestClassifier(
                n_estimators=config.RF_N_ESTIMATORS,
                max_depth=config.RF_MAX_DEPTH,
                random_state=config.RANDOM_STATE
            ))
        ])
        rf.fit(X_train, y_train)

        metrics = get_model_metrics(rf, X_test, y_test)

        # Log parameters
        mlflow.log_params({
            "model": "RandomForest",
            "n_estimators": 200,
            "max_depth": 6
        })

        # Log metrics
        mlflow.log_metrics(metrics)

        # Log plots
        log_plots(rf, X_test, y_test, "random_forest")

        # Log model
        model_info = mlflow.sklearn.log_model(rf, "random_forest")
        print(f"Random Forest Run ID: {mlflow.active_run().info.run_id}")
        print(f"Artifact URI: {mlflow.get_artifact_uri()}")
        print(f"Model URI: {model_info.model_uri}")

    print("MLflow experiment completed. Run 'mlflow ui' to view results.")
    return model_info.model_uri


if __name__ == "__main__":
    run_experiment()
