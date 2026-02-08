import pandas as pd
import numpy as np
import os

def create_dummy_data():
    # Columns typically found in CIC-IDS
    columns = [
        'Flow ID', 'Source IP', 'Source Port', 'Destination IP', 'Destination Port',
        'Protocol', 'Timestamp', 'Flow Duration', 'Total Fwd Packets',
        'Total Backward Packets', 'Total Length of Fwd Packets',
        'Total Length of Bwd Packets', 'Fwd Packet Length Max',
        'Fwd Packet Length Min', 'Fwd Packet Length Mean', 'Fwd Packet Length Std',
        'Bwd Packet Length Max', 'Bwd Packet Length Min', 'Bwd Packet Length Mean',
        'Bwd Packet Length Std', 'Flow Bytes/s', 'Flow Packets/s', 'Flow IAT Mean',
        'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min', 'Fwd IAT Total',
        'Fwd IAT Mean', 'Fwd IAT Std', 'Fwd IAT Max', 'Fwd IAT Min',
        'Bwd IAT Total', 'Bwd IAT Mean', 'Bwd IAT Std', 'Bwd IAT Max',
        'Bwd IAT Min', 'Fwd PSH Flags', 'Bwd PSH Flags', 'Fwd URG Flags',
        'Bwd URG Flags', 'Fwd Header Length', 'Bwd Header Length', 'Fwd Packets/s',
        'Bwd Packets/s', 'Min Packet Length', 'Max Packet Length',
        'Packet Length Mean', 'Packet Length Std', 'Packet Length Variance',
        'FIN Flag Count', 'SYN Flag Count', 'RST Flag Count', 'PSH Flag Count',
        'ACK Flag Count', 'URG Flag Count', 'CWE Flag Count', 'ECE Flag Count',
        'Down/Up Ratio', 'Average Packet Size', 'Avg Fwd Segment Size',
        'Avg Bwd Segment Size', 'Fwd Header Length.1', 'Fwd Avg Bytes/Bulk',
        'Fwd Avg Packets/Bulk', 'Fwd Avg Bulk Rate', 'Bwd Avg Bytes/Bulk',
        'Bwd Avg Packets/Bulk', 'Bwd Avg Bulk Rate', 'Subflow Fwd Packets',
        'Subflow Fwd Bytes', 'Subflow Bwd Packets', 'Subflow Bwd Bytes',
        'Init_Win_bytes_forward', 'Init_Win_bytes_backward', 'act_data_pkt_fwd',
        'min_seg_size_forward', 'Active Mean', 'Active Std', 'Active Max',
        'Active Min', 'Idle Mean', 'Idle Std', 'Idle Max', 'Idle Min', 'Label'
    ]
    
    # Generate 100 rows of random data
    data = []
    for i in range(100):
        row = {col: np.random.rand() * 100 for col in columns if col not in ['Flow ID', 'Source IP', 'Destination IP', 'Timestamp', 'Label']}
        row['Flow ID'] = f"192.168.1.{i}-10.0.0.{i}-80-443-6"
        row['Source IP'] = f"192.168.1.{i}"
        row['Destination IP'] = f"10.0.0.{i}"
        row['Timestamp'] = "01/01/2026 12:00:00"
        
        # Binary or Multiclass Label
        if i % 10 == 0:
            row['Label'] = "DDoS"
        elif i % 15 == 0:
            row['Label'] = "PortScan"
        else:
            row['Label'] = "BENIGN"
            
        data.append(row)
        
    df = pd.DataFrame(data)
    
    # Save to data/raw
    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/dummy_traffic.csv", index=False)
    print("Dummy dataset created at data/raw/dummy_traffic.csv")

if __name__ == "__main__":
    create_dummy_data()
