# Documentation & Reporting - Heart Disease MLOps

## 1. Setup & Installation Instructions

### Prerequisites
Ensure you have the following installed on your system:
*   **Python 3.9+**
*   **Docker Desktop** (with Kubernetes enabled)
*   **Git**

### Installation

1.  **Clone the Repository**
    ```bash
    git clone <repository-url>
    cd heart-disease-mlops-final
    ```

2.  **Set up Virtual Environment** (Recommended)
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Pipeline
The pipeline consists of modular scripts located in the `src/` directory. Run them in the following order:

1.  **Data Acquisition**: Downloads the dataset.
    ```bash
    python src/data_acquisition.py
    ```
2.  **Preprocessing**: Cleans data, handles missing values, and encodes categorical features.
    ```bash
    python src/preprocessing.py
    ```
3.  **Model Training**: Trains models (Logistic Regression & Random Forest) and outputs performance metrics.
    ```bash
    python src/train.py
    ```
4.  **Experiment Tracking**: Logs runs to MLflow.
    ```bash
    python src/experiment_tracking.py
    ```

---

## 2. EDA and Modelling Choices

### Exploratory Data Analysis (EDA)
EDA was performed to understand the dataset characteristics (see `notebooks/EDA.ipynb`). Key steps included:
*   **Data Cleaning**: 
    *   replaced `'?'` placeholders with `NaN`.
    *   Dropped rows with missing values.
*   **Feature Engineering**:
    *   Renamed columns to standard UCI Heart Disease names (e.g., `age`, `cp`, `trestbps`).
    *   Binarized the target variable: `0` (No Disease) vs `1-4` (Disease -> mapped to `1`).
*   **Encoding**: Label encoding was applied to categorical features such as `cp`, `restecg`, and `thal`.

### Modelling Choices
Two primary classification algorithms were selected for this binary classification task:

1.  **Logistic Regression**:
    *   Acts as a linear baseline.
    *   Pipeline includes `StandardScaler` to normalize features (critical for Logistic Regression).
    *   Hyperparameters: `max_iter=1000` to ensure convergence.

2.  **Random Forest Classifier**:
    *   Chosen for its ability to handle non-linear relationships and feature interactions.
    *   **Hyperparameter Tuning**: `GridSearchCV` (in `src/train.py`) was used to optimize:
        *   `n_estimators`: [100, 200]
        *   `max_depth`: [None, 6, 10]
        *   `min_samples_split`: [2, 5]

---

## 3. Experiment Tracking Summary

**Tool Used**: [MLflow](https://mlflow.org/)

Experiments are tracked in `src/experiment_tracking.py`. The MLOps pipeline logs the following for each run:

*   **Parameters**: Model type (e.g., "Logistic Regression"), hyperparameters (e.g., `n_estimators`, `max_depth`).
*   **Metrics**: Accuracy, Precision, Recall, F1-Score.
*   **Artifacts**:
    *   **Serialized Model**: The trained model object (pickle/sklearn format).
    *   **Confusion Matrix**: PNG image visualizing true vs. predicted labels.
    *   **ROC Curve**: PNG image showing trade-off between TPR and FPR.

To view the experiment dashboard:
```bash
mlflow ui
# Access at http://localhost:5000
```

---

## 4. Architecture Diagram

The following diagram illustrates the end-to-end MLOps pipeline architecture:

![Pipeline Architecture](image-1.png)

---

## 5. CI/CD and Deployment Workflows

The project uses **GitHub Actions** for automation.

### CI Workflow (`.github/workflows/ci.yml`)
Triggered on push/PR to `main`.
1.  **Setup**: Ubuntu runner, Python 3.9.
2.  **Linting**: checks code quality with `flake8`.
3.  **Data**: runs `data_acquisition.py`.
4.  **Testing**: runs unit tests with `pytest`.
5.  **Verification**: runs a sample training job.
6.  **Artifacts**: uploads model artifacts.

### CD Workflow (`.github/workflows/cd.yml`)
Triggered on push to `main` (after CI).
1.  **AWS Auth**: Configures credentials.
2.  **Containerize**: Builds Docker image (`heart-api`).
3.  **Registry**: Pushes image to Amazon ECR.
4.  **Deploy**: (Optional) Deploys to AWS App Runner or ECS.

### Workflow Visualization

![CI/CD Workflow](image-2.png)

### Deployment Screenshots

![AWS Deployment](image.png)

---

## 6. Link to Code Repository

**Repository URL**: `https://github.com/ssrikantasahoo/heart-disease-mlops-final`

---

## 7. Pipeline Demo Video

The following video demonstrates the execution of the pipeline, including MLflow experiment tracking and artifact inspection.

![Pipeline Demo](pipeline_full.gif)
