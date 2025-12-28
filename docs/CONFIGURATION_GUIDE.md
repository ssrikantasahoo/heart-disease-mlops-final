# Configuration Guide

## Overview

The Heart Disease MLOps project now uses a centralized configuration system via `src/config.py`. All previously hardcoded values can be customized using environment variables.

## Configuration Module

### Location
`src/config.py`

### Usage
```python
from config import config

# Access configuration values
data_path = config.CSV_PATH
experiment_name = config.EXPERIMENT_NAME
random_state = config.RANDOM_STATE
```

## Available Configuration Options

### Data Configuration

| Environment Variable | Default Value | Description |
|---------------------|---------------|-------------|
| `DATA_URL` | `https://archive.ics.uci.edu/...` | UCI Heart Disease dataset URL |
| `DATA_DIR` | `data` | Directory for storing data files |
| `CSV_FILENAME` | `heart.csv` | Name of the CSV file |
| `TARGET_DATA_FILE` | `processed.cleveland.data` | Target data file from UCI archive |

### MLflow Configuration

| Environment Variable | Default Value | Description |
|---------------------|---------------|-------------|
| `MLFLOW_EXPERIMENT_NAME` | `heart-disease-experiment` | MLflow experiment name |
| `MLRUNS_DIR` | `mlruns` | MLflow runs directory |
| `MLFLOW_TRACKING_URI` | Auto-generated | MLflow tracking URI (file-based) |

### Model Configuration

| Environment Variable | Default Value | Description |
|---------------------|---------------|-------------|
| `RANDOM_STATE` | `42` | Random seed for reproducibility |
| `TEST_SIZE` | `0.2` | Train/test split ratio |
| `CV_FOLDS` | `5` | Cross-validation folds |
| `PRODUCTION_MODEL_DIR` | `models/production_model` | Production model output directory |

### Logistic Regression Hyperparameters

| Environment Variable | Default Value | Description |
|---------------------|---------------|-------------|
| `LOGREG_MAX_ITER` | `1000` | Maximum iterations for LogisticRegression |

### Random Forest Hyperparameters

| Environment Variable | Default Value | Description |
|---------------------|---------------|-------------|
| `RF_N_ESTIMATORS` | `200` | Number of trees in Random Forest |
| `RF_MAX_DEPTH` | `6` | Maximum depth of trees |
| `RF_MIN_SAMPLES_SPLIT` | `5` | Minimum samples to split a node |

### GridSearch Configuration

| Environment Variable | Default Value | Description |
|---------------------|---------------|-------------|
| `GRID_N_JOBS` | `-1` | Number of parallel jobs for GridSearch |

### API Configuration

| Environment Variable | Default Value | Description |
|---------------------|---------------|-------------|
| `API_TITLE` | `Heart Disease Prediction API` | API title |
| `API_DESCRIPTION` | `FastAPI service for...` | API description |
| `API_VERSION` | `1.0` | API version |
| `API_HOST` | `0.0.0.0` | API host address |
| `API_PORT` | `8000` | API port number |

### CORS Configuration

| Environment Variable | Default Value | Description |
|---------------------|---------------|-------------|
| `CORS_ALLOW_ORIGINS` | `*` | Allowed CORS origins (comma-separated) |
| `CORS_ALLOW_CREDENTIALS` | `true` | Allow credentials in CORS |

### Logging Configuration

| Environment Variable | Default Value | Description |
|---------------------|---------------|-------------|
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `LOG_FORMAT` | `%(asctime)s — %(levelname)s — %(message)s` | Log message format |

## Usage Examples

### Example 1: Custom Random Seed and Test Size

**Windows (PowerShell):**
```powershell
$env:RANDOM_STATE = "123"
$env:TEST_SIZE = "0.3"
python src\experiment_tracking.py
```

**Linux/Mac:**
```bash
export RANDOM_STATE=123
export TEST_SIZE=0.3
python src/experiment_tracking.py
```

### Example 2: Custom API Port

**Windows (PowerShell):**
```powershell
$env:API_PORT = "9000"
uvicorn src.app:app --host 0.0.0.0 --port 9000
```

**Linux/Mac:**
```bash
export API_PORT=9000
uvicorn src.app:app --host 0.0.0.0 --port $API_PORT
```

### Example 3: Custom Data Directory

**Windows (PowerShell):**
```powershell
$env:DATA_DIR = "custom_data"
python src\data_acquisition.py
```

**Linux/Mac:**
```bash
export DATA_DIR=custom_data
python src/data_acquisition.py
```

### Example 4: Production CORS Configuration

**Windows (PowerShell):**
```powershell
$env:CORS_ALLOW_ORIGINS = "https://myapp.com,https://admin.myapp.com"
$env:LOG_LEVEL = "WARNING"
uvicorn src.app:app
```

**Linux/Mac:**
```bash
export CORS_ALLOW_ORIGINS="https://myapp.com,https://admin.myapp.com"
export LOG_LEVEL="WARNING"
uvicorn src.app:app
```

### Example 5: Docker with Custom Port

```bash
# Build with custom port
docker build --build-arg API_PORT=9000 -t heart-disease-api .

# Run with custom port
docker run -p 9000:9000 -e API_PORT=9000 heart-disease-api
```

### Example 6: Custom Model Hyperparameters

**Windows (PowerShell):**
```powershell
$env:RF_N_ESTIMATORS = "300"
$env:RF_MAX_DEPTH = "10"
$env:LOGREG_MAX_ITER = "2000"
python src\experiment_tracking.py
```

**Linux/Mac:**
```bash
export RF_N_ESTIMATORS=300
export RF_MAX_DEPTH=10
export LOGREG_MAX_ITER=2000
python src/experiment_tracking.py
```

## Viewing Current Configuration

To see all current configuration values:

```bash
python src/config.py
```

This will display all configuration settings with their current values (including any environment variable overrides).

## Migration from Hardcoded Values

All hardcoded values have been removed from the following files:

- ✅ `src/data_acquisition.py` - Data paths and URLs
- ✅ `src/preprocessing.py` - Column definitions (fixed duplicate path bug)
- ✅ `src/train.py` - Model hyperparameters, test size, random state
- ✅ `src/experiment_tracking.py` - Experiment name, model parameters
- ✅ `src/model_packaging.py` - Production model path, hyperparameters
- ✅ `src/app.py` - API settings, CORS configuration
- ✅ `src/model_utils.py` - CV folds
- ✅ `src/inference_pipeline.py` - Dynamic model discovery
- ✅ `Dockerfile` - Configurable port

## Best Practices

1. **Development**: Use defaults by not setting any environment variables
2. **Testing**: Override specific values as needed for test scenarios
3. **Production**: Set environment variables for production-specific configurations
4. **Security**: Never commit `.env` files with sensitive configurations
5. **Documentation**: Document any custom environment variables you add

## Troubleshooting

### Issue: Configuration not updating

**Solution**: Ensure environment variables are set before importing the config module. Python caches imports, so restart your Python process if needed.

### Issue: Type errors with environment variables

**Solution**: Environment variables are always strings. The config module handles type conversion automatically (int, float, bool, list).

### Issue: CORS not working as expected

**Solution**: For multiple origins, use comma-separated values:
```bash
export CORS_ALLOW_ORIGINS="http://localhost:3000,https://myapp.com"
```

## Adding New Configuration

To add a new configuration option:

1. Add it to `src/config.py` in the appropriate section:
```python
NEW_SETTING: str = os.getenv("NEW_SETTING", "default_value")
```

2. Use it in your code:
```python
from config import config
value = config.NEW_SETTING
```

3. Document it in this guide
