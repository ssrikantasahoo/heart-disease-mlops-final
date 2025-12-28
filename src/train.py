import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from config import config
from model_utils import (
    get_model_metrics,
    run_cross_validation,
    comparison_table
)

from preprocessing import clean_dataset


def train_models():
    """
    Train Logistic Regression and Random Forest models with:
    - Scaling
    - CV
    - Metrics evaluation
    - MLflow logging
    Returns trained models as dict.
    """

    # Load data
    df = pd.read_csv(config.CSV_PATH)
    df = clean_dataset(df)

    X = df.drop("target", axis=1)
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=config.TEST_SIZE, random_state=config.RANDOM_STATE
    )

    # ------------------------
    # 1. Logistic Regression
    # ------------------------
    log_reg_pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter=config.LOGREG_MAX_ITER, random_state=config.RANDOM_STATE))
    ])

    log_reg_pipe.fit(X_train, y_train)

    log_reg_metrics = get_model_metrics(log_reg_pipe, X_test, y_test)
    log_reg_cv = run_cross_validation(log_reg_pipe, X, y)

    # ------------------------
    # 2. Random Forest (with Tuning)
    # ------------------------
    rf_pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("model", RandomForestClassifier(random_state=42))
    ])

    # Hyperparameter tuning using GridSearchCV
    param_grid = {
        'model__n_estimators': config.GRID_N_ESTIMATORS,
        'model__max_depth': config.GRID_MAX_DEPTH,
        'model__min_samples_split': config.GRID_MIN_SAMPLES_SPLIT
    }

    from sklearn.model_selection import GridSearchCV
    grid_search = GridSearchCV(rf_pipe, param_grid, cv=config.CV_FOLDS, scoring='accuracy', n_jobs=config.GRID_N_JOBS)
    grid_search.fit(X_train, y_train)

    best_rf_model = grid_search.best_estimator_
    print(f"Best RF Params: {grid_search.best_params_}")

    rf_metrics = get_model_metrics(best_rf_model, X_test, y_test)
    rf_cv = run_cross_validation(best_rf_model, X, y)

    # ------------------------
    # Comparison Table
    # ------------------------
    results = {
        "Logistic Regression": {
            **log_reg_metrics,
            "cv_accuracy": log_reg_cv
        },
        "Random Forest": {
            **rf_metrics,
            "cv_accuracy": rf_cv
        }
    }

    table = comparison_table(results)
    print("\n=== Model Comparison Table ===")
    print(table)

    return {
        "log_reg_model": log_reg_pipe,
        "random_forest_model": best_rf_model,
        "comparison_table": table
    }


if __name__ == "__main__":
    train_models()
