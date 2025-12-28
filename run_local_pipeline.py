#!/usr/bin/env python
"""
Cross-platform pipeline runner for Heart Disease MLOps project.
Works on Windows, Linux, and Mac.
"""
import subprocess
import sys


def run_step(step_num, total_steps, description, command):
    """Run a pipeline step and handle errors."""
    print(f"\n[{step_num}/{total_steps}] {description}...")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"\nError: {description} failed with exit code {result.returncode}")
        sys.exit(result.returncode)


def main():
    print("=" * 50)
    print("Starting Local Heart Disease MLOps Pipeline")
    print("=" * 50)

    steps = [
        (1, 6, "Running Data Acquisition", "python src/data_acquisition.py"),
        (2, 6, "Running Preprocessing", "python src/preprocessing.py"),
        (3, 6, "Running Model Training", "python src/train.py"),
        (4, 6, "Running Experiment Tracking (MLflow)", "python src/experiment_tracking.py"),
        (5, 6, "Running Model Packaging", "python src/model_packaging.py"),
        (6, 6, "Running Unit Tests", "python -m pytest tests/"),
    ]

    for step in steps:
        run_step(*step)

    print("\n" + "=" * 50)
    print("Pipeline Completed Successfully!")
    print("=" * 50)
    print("To view MLflow results, run: mlflow ui")
    print("To run the API locally, run: uvicorn src.app:app --reload")


if __name__ == "__main__":
    main()
