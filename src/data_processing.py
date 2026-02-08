import pandas as pd
import numpy as np
import os
import glob
from sklearn.preprocessing import LabelEncoder

RAW_DATA_PATH = os.path.join("data", "raw")
PROCESSED_DATA_PATH = os.path.join("data", "processed")

def load_data():
    """Loads and merges all CSV files from data/raw."""
    all_files = glob.glob(os.path.join(RAW_DATA_PATH, "*.csv"))
    
    if not all_files:
        print(f"No CSV files found in {RAW_DATA_PATH}. Please place dataset files there.")
        return None

    df_list = []
    for filename in all_files:
        print(f"Loading {filename}...")
        df = pd.read_csv(filename)
        df_list.append(df)

    if not df_list:
        return None
        
    combined_df = pd.concat(df_list, ignore_index=True)
    print(f"Total shape: {combined_df.shape}")
    return combined_df

def clean_data(df):
    """
    1. Removes whitespace from column names.
    2. Drops unnecessary columns.
    3. Handles infinity and missing values.
    """
    # 1. Strip whitespace from column names
    df.columns = df.columns.str.strip()
    
    # 2. Drop columns
    drop_cols = ['Flow ID', 'Source IP', 'Destination IP', 'Timestamp']
    # Only drop if they exist
    existing_drop_cols = [c for c in drop_cols if c in df.columns]
    if existing_drop_cols:
        print(f"Dropping columns: {existing_drop_cols}")
        df.drop(columns=existing_drop_cols, inplace=True)
    
    # 3. Replace inf with nan and drop
    print("Handling infinity and NaNs...")
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)
    
    print(f"Shape after cleaning: {df.shape}")
    return df

def encode_labels(df):
    """Encodes the 'Label' column."""
    if 'Label' not in df.columns:
        print("Warning: 'Label' column not found.")
        return df, None
        
    le = LabelEncoder()
    df['Label_Encoded'] = le.fit_transform(df['Label'])
    
    # Print mapping
    mapping = dict(zip(le.classes_, le.transform(le.classes_)))
    print("Label Mapping:")
    for k, v in mapping.items():
        print(f"  {k} -> {v}")
        
    return df, le

def main():
    # Ensure directories exist
    os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)
    
    # 1. Load
    df = load_data()
    if df is None:
        return

    # 2. Clean
    df = clean_data(df)
    
    # Save clean data (before encoding if you want to keep original labels for visualization)
    clean_path = os.path.join(PROCESSED_DATA_PATH, "clean_data.csv")
    print(f"Saving cleaned data to {clean_path}...")
    df.to_csv(clean_path, index=False)
    
    # 3. Encode
    df_encoded, le = encode_labels(df)
    
    if le:
        # Save training data
        train_path = os.path.join(PROCESSED_DATA_PATH, "train_encoded.csv")
        print(f"Saving encoded data to {train_path}...")
        df_encoded.to_csv(train_path, index=False)

if __name__ == "__main__":
    main()
