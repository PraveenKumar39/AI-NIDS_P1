import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

PROCESSED_DATA_PATH = os.path.join("data", "processed")
MODELS_PATH = os.path.join("models")

def load_data():
    """Loads the encoded training data."""
    file_path = os.path.join(PROCESSED_DATA_PATH, "train_encoded.csv")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found. Please run data_processing.py first.")
    
    df = pd.read_csv(file_path)
    return df

def train_model():
    # 1. Load data
    df = load_data()
    
    # 2. Separate Features and Target
    if 'Label_Encoded' not in df.columns:
        raise ValueError("Label_Encoded column missing.")
        
    X = df.drop(columns=['Label', 'Label_Encoded'])
    y = df['Label_Encoded']
    
    print(f"Features: {X.shape}, Target: {y.shape}")
    
    # 3. Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    print(f"Train size: {X_train.shape[0]}, Test size: {X_test.shape[0]}")
    
    # 4. Train Model
    print("Training RandomForestClassifier...")
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    
    # 5. Evaluate
    print("Evaluating model...")
    y_pred = rf.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    # Use average='weighted' for multiclass
    prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    
    print(f"\n--- Metrics ---")
    print(f"Accuracy:  {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall:    {rec:.4f}")
    print(f"F1 Score:  {f1:.4f}")
    
    print("\n--- Confusion Matrix ---")
    print(confusion_matrix(y_test, y_pred))
    
    print("\n--- Classification Report ---")
    print(classification_report(y_test, y_pred, zero_division=0))
    
    # 6. Save Model
    os.makedirs(MODELS_PATH, exist_ok=True)
    model_path = os.path.join(MODELS_PATH, "model.pkl")
    joblib.dump(rf, model_path)
    print(f"\nModel saved to {model_path}")

if __name__ == "__main__":
    train_model()
