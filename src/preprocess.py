import pandas as pd
import numpy as np
import os
import glob
from sklearn.preprocessing import LabelEncoder
import joblib

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
ENCODER_PATH = "models/label_encoder.pkl"

def load_and_merge_data():
    """Merges all CSVs in data/raw."""
    all_files = glob.glob(os.path.join(RAW_DIR, "*.csv"))
    if not all_files:
        print("No data found in data/raw/")
        return None
    
    df_list = []
    for filename in all_files:
        print(f"Loading {filename}...")
        df = pd.read_csv(filename, index_col=None, header=0)
        df_list.append(df)
        
    df = pd.concat(df_list, axis=0, ignore_index=True)
    print(f"Total shape: {df.shape}")
    return df

def clean_data(df):
    """Cleans columns and handles NaNs."""
    # Strip whitespace from columns
    df.columns = df.columns.str.strip()
    
    # Drop identifiers
    drop_cols = ['Flow ID', 'Source IP', 'Destination IP', 'Timestamp']
    df = df.drop(columns=[c for c in drop_cols if c in df.columns], errors='ignore')
    
    # Handle infinite/NaN
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna()
    
    print(f"Shape after cleaning: {df.shape}")
    return df

def encode_labels(df):
    """Encodes Label column and saves the encoder."""
    le = LabelEncoder()
    df['Label_Encoded'] = le.fit_transform(df['Label'])
    
    # Save mapping for reference
    mapping = dict(zip(le.classes_, le.transform(le.classes_)))
    print("Label Mapping:")
    for k, v in mapping.items():
        print(f"  {k} -> {v}")
        
    # Save encoder
    os.makedirs(os.path.dirname(ENCODER_PATH), exist_ok=True)
    joblib.dump(le, ENCODER_PATH)
    
    return df

def process_pipeline():
    """Runs the full preprocessing pipeline."""
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    
    df = load_and_merge_data()
    if df is not None:
        df = clean_data(df)
        df = encode_labels(df)
        
        output_path = os.path.join(PROCESSED_DIR, "train_encoded.csv")
        df.to_csv(output_path, index=False)
        print(f"Saved processed data to {output_path}")

if __name__ == "__main__":
    process_pipeline()
