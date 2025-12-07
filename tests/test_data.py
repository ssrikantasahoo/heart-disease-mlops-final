import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from preprocessing import clean_dataset  # noqa: E402


def test_clean_dataset():
    df = pd.DataFrame({
        "age": [50, 60],
        "sex": ["1", "0"],
        "cp": ["1", "2"],
        "trestbps": [140, 150],
        "chol": [250, 260],
        "fbs": ["0", "1"],
        "restecg": ["0", "1"],
        "thalach": [160, 170],
        "exang": ["0", "1"],
        "oldpeak": [1.0, 2.3],
        "slope": ["1", "2"],
        "ca": ["0", "1"],
        "thal": ["2", "3"],
        "target": [1, 0]
    })

    df_clean = clean_dataset(df)
    assert df_clean.isna().sum().sum() == 0
    assert df_clean.shape[0] == 2
    assert df_clean.shape[1] == 14

    # Check binarization: target 0->0, 1->1 (and 2,3,4->1)
    # In input we had 1 and 0.
    # Let's add a case for >1
    df2 = pd.DataFrame({
        "age": [50], "sex": ["1"], "cp": ["1"], "trestbps": [140], "chol": [250],
        "fbs": ["0"], "restecg": ["0"], "thalach": [160], "exang": ["0"],
        "oldpeak": [1.0], "slope": ["1"], "ca": ["0"], "thal": ["2"],
        "target": [3]  # Should become 1
    })
    df2_clean = clean_dataset(df2)
    assert df2_clean['target'].iloc[0] == 1
