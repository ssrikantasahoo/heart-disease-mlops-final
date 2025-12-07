@echo off
echo ==========================================
echo Starting Local Heart Disease MLOps Pipeline
echo ==========================================

echo.
echo [1/6] Running Data Acquisition...
python src/data_acquisition.py
if %errorlevel% neq 0 exit /b %errorlevel%

echo.
echo [2/6] Running Preprocessing...
python src/preprocessing.py
if %errorlevel% neq 0 exit /b %errorlevel%

echo.
echo [3/6] Running Model Training...
python src/train.py
if %errorlevel% neq 0 exit /b %errorlevel%

echo.
echo [4/6] Running Experiment Tracking (MLflow)...
python src/experiment_tracking.py
if %errorlevel% neq 0 exit /b %errorlevel%

echo.
echo [5/6] Running Model Packaging...
python src/model_packaging.py
if %errorlevel% neq 0 exit /b %errorlevel%

echo.
echo [6/6] Running Unit Tests...
python -m pytest tests/
if %errorlevel% neq 0 exit /b %errorlevel%

echo.
echo ==========================================
echo Pipeline Completed Successfully!
echo ==========================================
echo To view MLflow results, run: mlflow ui
echo To run the API locally, run: uvicorn src.app:app --reload
pause
