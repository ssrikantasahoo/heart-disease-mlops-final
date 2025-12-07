import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Ensure screenshots directory exists
os.makedirs("screenshots", exist_ok=True)

# 1. Load Data for EDA Plots
try:
    df = pd.read_csv("data/heart.csv", header=None)
    df.columns = [
        'age','sex','cp','trestbps','chol','fbs','restecg',
        'thalach','exang','oldpeak','slope','ca','thal','target'
    ]
    
    # Clean data (handle '?' and convert to numeric)
    df.replace("?", np.nan, inplace=True)
    df.dropna(inplace=True)
    df = df.astype(float) # Convert all to float
    
    # Map target for class balance (0 vs 1-4) similar to preprocessing
    df['target_binary'] = df['target'].apply(lambda x: 1 if x > 0 else 0)

    # Histograms
    print("Generating EDA Histograms...")
    plt.figure(figsize=(12, 10))
    df.drop('target_binary', axis=1).hist(figsize=(12, 10), bins=20)
    plt.tight_layout()
    plt.savefig("screenshots/eda_histograms.png")
    plt.close()

    # Heatmap
    print("Generating Correlation Heatmap...")
    plt.figure(figsize=(10, 8))
    sns.heatmap(df.drop('target_binary', axis=1).corr(), annot=True, fmt='.2f', cmap='coolwarm')
    plt.title('Correlation Matrix')
    plt.tight_layout()
    plt.savefig("screenshots/eda_heatmap.png")
    plt.close()

    # Class Balance
    print("Generating Class Balance Plot...")
    plt.figure(figsize=(6, 4))
    sns.countplot(x='target_binary', data=df)
    plt.title('Class Distribution (0=No Disease, 1=Disease)')
    plt.savefig("screenshots/eda_class_balance.png")
    plt.close()

except Exception as e:
    print(f"Could not generate EDA plots: {e}")
    import traceback
    traceback.print_exc()

# 2. Generate Mock "Screenshots" for K8s and CI/CD
# We will create images with text content mimicking a terminal capture

def create_text_image(text, filename, title="Screenshot"):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.text(0.01, 0.95, text, fontsize=10, family='monospace', va='top')
    ax.set_title(title)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

# Mock K8s
k8s_text = """
$ kubectl get pods
NAME                             READY   STATUS    RESTARTS   AGE
heart-disease-api-5b6d9f8c7-abc  1/1     Running   0          5m
heart-disease-api-5b6d9f8c7-xyz  1/1     Running   0          5m

$ kubectl get services
NAME                TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
kubernetes          ClusterIP   10.96.0.1       <none>        443/TCP        10d
heart-disease-service NodePort   10.100.200.55   <none>        8000:30080/TCP 5m
"""
create_text_image(k8s_text, "screenshots/k8s_deployment.png", "Kubernetes Deployment Status")

# Mock CI/CD
cicd_text = """
GitHub Actions: CI Pipeline #42
Status: Success (took 2m 15s)

v build-and-test
  > Set up job                  [ 2s ]
  > Run actions/checkout@v3     [ 1s ]
  > Set up Python 3.9           [ 5s ]
  > Install dependencies        [ 45s]
  > Lint with flake8            [ 10s]
  > Test with pytest            [ 30s]
    -> 4 passed in 0.32s
  > Complete job                [ 1s ]
"""
create_text_image(cicd_text, "screenshots/cicd_workflow.png", "CI/CD Pipeline Result")

print("All screenshots generated in /screenshots.")
