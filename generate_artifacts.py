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
import shutil


def get_gh_path():
    """Get the path to gh CLI executable"""
    # Try to find gh in PATH
    gh_path = shutil.which("gh")
    if gh_path:
        return f'"{gh_path}"'
    
    # Fallback to common Windows installation path
    common_path = "C:\\Program Files\\GitHub CLI\\gh.exe"
    import os
    if os.path.exists(common_path):
        return f'& "{common_path}"'
    
    # If not found, just return 'gh' and hope it's in PATH
    return "gh"


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
    # First, check if gh CLI is available
    gh_cmd = get_gh_path()
    gh_check = run_command(f"{gh_cmd} --version 2>&1")
    
    if "not found" in gh_check.lower() or "not recognized" in gh_check.lower():
        # Fallback: Use git log to show recent activity
        cicd_text = """GitHub Actions: CI/CD Pipeline
Note: Install 'gh' CLI for live pipeline status
Run: gh auth login

Recent Git Activity:
"""
        git_log = run_command("git log --oneline -5 2>&1")
        cicd_text += git_log
    else:
        # Use simple text-based output (no JSON parsing needed)
        print("  → Fetching workflow list...")
        workflow_list = run_command(f"{gh_cmd} run list --limit 5 2>&1")
        
        print("  → Fetching latest run ID...")
        # Extract the first run ID from the list (non-interactive)
        # The output format is: STATUS  TITLE  WORKFLOW  BRANCH  EVENT  ID  ELAPSED  AGE
        # But headers are abbreviated: ST  TI  WO  BR  EV  ID  EL  AG
        run_id_output = run_command(f"{gh_cmd} run list --limit 1 2>&1")
        
        # Try to extract run ID from the output
        run_id = None
        lines = run_id_output.strip().split('\n')
        
        # Skip header line and process data lines
        for line in lines:
            if line.strip() and not line.startswith('ST') and not line.startswith('STATUS'):
                # Split by multiple spaces/tabs to get columns
                parts = line.split()
                # The ID column is typically the 6th column (index 5)
                # Look for a numeric value that looks like a run ID
                for part in parts:
                    # Run IDs are typically large numbers
                    if part.isdigit() and len(part) >= 2:
                        run_id = part
                        break
                if run_id:
                    break
        
        print(f"  → Fetching details for run ID: {run_id}...")
        # Get the most recent workflow run details using the extracted ID
        if run_id:
            run_details = run_command(f"{gh_cmd} run view {run_id} 2>&1")
        else:
            run_details = "Could not extract run ID. Using workflow list only."
        
        # Build comprehensive CI/CD text
        cicd_text = f"""GitHub Actions: CI/CD Pipeline Status

=== Latest Workflow Run Details ===
{run_details}

=== Recent Workflow Runs ===
{workflow_list}

Commands:
  - View specific run: gh run view <run-id>
  - Watch live run: gh run watch
  - View logs: gh run view --log
"""
    
    create_text_image(cicd_text, "screenshots/cicd_workflow.png", "CI/CD Pipeline Status")
    print("✓ CI/CD screenshot generated")
except Exception as e:
    print(f"Could not generate CI/CD screenshot: {e}")
    import traceback
    traceback.print_exc()

print("All screenshots generated in /screenshots.")
