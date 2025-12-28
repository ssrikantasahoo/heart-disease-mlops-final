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
        'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
        'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target'
    ]
    # Clean data (handle '?' and convert to numeric)
    df.replace("?", np.nan, inplace=True)
    df.dropna(inplace=True)
    df = df.astype(float)  # Convert all to float

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


# 2. Generate Real Screenshots for K8s and CI/CD
# Fetch actual data from running Kubernetes cluster and CI/CD pipeline

import subprocess


def create_text_image(text, filename, title="Screenshot"):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.text(0.01, 0.95, text, fontsize=10, family='monospace', va='top')
    ax.set_title(title)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


def run_command(command):
    """Execute shell command and return output"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return f"Error executing command: {e}"


# Fetch Real K8s Data
print("Fetching Kubernetes deployment status...")
try:
    pods_output = run_command("kubectl get pods")
    services_output = run_command("kubectl get services")
    
    k8s_text = f"""$ kubectl get pods
{pods_output}
$ kubectl get services
{services_output}"""
    
    create_text_image(k8s_text, "screenshots/k8s_deployment.png", "Kubernetes Deployment Status")
    print("✓ Kubernetes screenshot generated")
except Exception as e:
    print(f"Could not generate K8s screenshot: {e}")

# Fetch Real CI/CD Data (GitHub Actions latest workflow run)
print("Fetching CI/CD pipeline status...")
try:
    # Try to get latest GitHub Actions workflow status
    # This requires gh CLI to be installed and authenticated
    workflow_output = run_command("gh run list --limit 1 2>&1")
    
    if "gh: command not found" in workflow_output or "not found" in workflow_output.lower():
        # Fallback: Use git log to show recent activity
        cicd_text = """GitHub Actions: CI/CD Pipeline
Note: Install 'gh' CLI for live pipeline status
Run: gh auth login

Recent Git Activity:
"""
        git_log = run_command("git log --oneline -5 2>&1")
        cicd_text += git_log
    else:
        cicd_text = f"""GitHub Actions: Latest Workflow Runs
{workflow_output}

For detailed run info, use: gh run view <run-id>
"""
    
    create_text_image(cicd_text, "screenshots/cicd_workflow.png", "CI/CD Pipeline Status")
    print("✓ CI/CD screenshot generated")
except Exception as e:
    print(f"Could not generate CI/CD screenshot: {e}")

print("All screenshots generated in /screenshots.")
