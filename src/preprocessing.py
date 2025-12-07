import pandas as pd
from sklearn.preprocessing import LabelEncoder

def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans Heart Disease dataset:
    - Replace '?' with NaN
    - Drop rows with missing values
    - Encode categorical variables
    """
    df.replace("?", pd.NA, inplace=True)
    df.dropna(inplace=True)

    # UCI column documentation has 14+ columns; enforce consistent names
    df.columns = [
        'age','sex','cp','trestbps','chol','fbs','restecg',
        'thalach','exang','oldpeak','slope','ca','thal','target'
    ]

    categorical_cols = ['cp','restecg','slope','thal','sex','fbs','exang','ca']

    for col in categorical_cols:
        df[col] = LabelEncoder().fit_transform(df[col].astype(str))

    df = df.astype(float)
    
    # Binarize target: 0 = No Disease, 1-4 = Disease
    df['target'] = df['target'].apply(lambda x: 1 if x > 0 else 0)
    
    return df

if __name__ == "__main__":
    path = "data/heart.csv"
    path = "data/heart.csv"
    # Read without header as data_acquisition saves it raw
    df = pd.read_csv(path, header=None)
    df_clean = clean_dataset(df)
    print(df_clean.head())
