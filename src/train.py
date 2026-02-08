import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from xgboost import XGBClassifier

DATA_PATH = "data/processed/train_encoded.csv"
MODEL_DIR = "models"

def load_data():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"{DATA_PATH} not found. Run preprocess.py first.")
    
    df = pd.read_csv(DATA_PATH)
    return df

def train_models():
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    print("Loading data...")
    df = load_data()
    
    # Stratified Split
    X = df.drop(columns=['Label', 'Label_Encoded'])
    y = df['Label_Encoded']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Save test set for evaluation
    test_data = X_test.copy()
    test_data['Label_Encoded'] = y_test
    test_data.to_csv(os.path.join(MODEL_DIR, "test_set.csv"), index=False)
    print(f"Saved test set to {MODEL_DIR}/test_set.csv")

    # --- 1. Random Forest ---
    print("\nTraining Random Forest...")
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    joblib.dump(rf, os.path.join(MODEL_DIR, "rf_model.pkl"))
    print("Saved rf_model.pkl")

    # --- 2. XGBoost ---
    print("\nTraining XGBoost...")
    xgb = XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=42)
    xgb.fit(X_train, y_train)
    joblib.dump(xgb, os.path.join(MODEL_DIR, "xgb_model.pkl"))
    print("Saved xgb_model.pkl")

    # --- 3. Isolation Forest (Anomaly Detection) ---
    print("\nTraining Isolation Forest...")
    # IsoForest is unsupervised. We train it on efficiently "normal" data or all data to find outliers.
    # Here we train on X_train. It usually requires different handling for prediction (-1 outlier, 1 inlier).
    iso = IsolationForest(contamination=0.1, random_state=42)
    iso.fit(X_train)
    joblib.dump(iso, os.path.join(MODEL_DIR, "iso_model.pkl"))
    print("Saved iso_model.pkl")
    
    print("\nAll models trained and saved.")

if __name__ == "__main__":
    train_models()
