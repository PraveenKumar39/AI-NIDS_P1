import pandas as pd
import joblib
import time
import os
import yaml
from datetime import datetime

class RealTimeDetector:
    def __init__(self, model_path="models/rf_model.pkl", config_path="config/risk_rules.yaml"):
        self.model = joblib.load(model_path)
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.label_map = {0: "BENIGN", 1: "DDoS", 2: "PortScan"}

    def calculate_risk(self, label_idx, prob):
        label_name = self.label_map.get(label_idx, "Unknown")
        rules = self.config.get('risk_mapping', {}).get(label_name, self.config.get('default', {}))
        
        base_risk = rules.get('base_risk', 50)
        max_risk = rules.get('max_risk', 50)
        
        risk = base_risk + (prob * (max_risk - base_risk))
        risk = min(int(risk), 100)
        
        if risk <= 20: s = "Safe"
        elif risk <= 50: s = "Medium"
        elif risk <= 80: s = "High"
        else: s = "Critical"
        
        return risk, s, label_name

    def stream_traffic(self, csv_path, delay=0.5):
        if not os.path.exists(csv_path):
            print(f"File {csv_path} not found.")
            return

        print(f"[INFO] Starting Real-Time Detection Simulation on {csv_path}...")
        print("Press Ctrl+C to stop.\n")
        
        # Load data chunk (simulate stream)
        df_iter = pd.read_csv(csv_path, chunksize=1)
        
        # Columns used for training (ensure alignment)
        # Assuming the CSV has the same structure as training data (minus label)
        # For demo purposes, we drop non-feature cols if present
        
        for i, df_chunk in enumerate(df_iter):
            try:
                # Preprocess row (drop labels for prediction)
                cols_to_drop = ['Label', 'Label_Encoded', 'Flow ID', 'Source IP', 'Destination IP', 'Timestamp']
                X = df_chunk.drop(columns=[c for c in cols_to_drop if c in df_chunk.columns], errors='ignore')
                
                # Predict
                pred = self.model.predict(X)[0]
                prob = self.model.predict_proba(X)[0][pred]
                
                risk, severity, attack_type = self.calculate_risk(pred, prob)
                
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                if attack_type != "BENIGN":
                    print(f"[ALERT] {timestamp}")
                    print(f"   Type:      {attack_type}")
                    print(f"   Confidence: {prob*100:.1f}%")
                    print(f"   Severity:   {severity} (Risk: {risk})")
                    print("-" * 30)
                else:
                    # Optional: Print benign traffic sparsely
                    if i % 10 == 0:
                        print(f"[SAFE] {timestamp} - Normal Traffic")
                
                time.sleep(delay)
                
            except KeyboardInterrupt:
                print("\n[STOP] Simulation stopped.")
                break
            except Exception as e:
                print(f"Error processing row: {e}")
                continue

if __name__ == "__main__":
    detector = RealTimeDetector()
    # Use demo data if available, else test set
    target_file = "data/raw/demo_attack_heavy.csv"
    if not os.path.exists(target_file):
        target_file = "models/test_set.csv"
        
    detector.stream_traffic(target_file, delay=0.2)
