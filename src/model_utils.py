from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
import pandas as pd


def get_model_metrics(model, X_test, y_test):
    """
    Returns a dict of evaluation metrics.
    """
    y_pred = model.predict(X_test)
    if hasattr(model, "predict_proba"):
        y_prob = model.predict_proba(X_test)[:, 1]
    else:
        y_prob = model.decision_function(X_test)

    return {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_prob)
    }


def run_cross_validation(model, X, y, cv=5):
    """
    Computes CV accuracy scores.
    """
    scores = cross_val_score(model, X, y, cv=cv, scoring="accuracy")
    return scores.mean()


def comparison_table(results_dict):
    """
    Converts model metric results into a single table.
    """
    return pd.DataFrame(results_dict).T
