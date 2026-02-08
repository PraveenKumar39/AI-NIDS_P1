import requests
import time
import sys

BASE_URL = "http://127.0.0.1:8000"
API_KEY = "secret-key-123"

def test_health():
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("[OK] Health Check Passed")
            return True
        else:
            print(f"[FAIL] Health Check Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] Health Check Error: {e}")
        return False

def test_prediction():
    headers = {"X-API-Key": API_KEY}
    payload = {
        "Destination Port": 80,
        "Flow Duration": 1000,
        "Total Fwd Packets": 10
    }
    
    try:
        response = requests.post(f"{BASE_URL}/v1/predict", json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print("[OK] Prediction Passed")
            print(f"   Response: {data}")
            return True
        else:
            print(f"[FAIL] Prediction Failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Prediction Error: {e}")
        return False

if __name__ == "__main__":
    print("Waiting for API to start...")
    time.sleep(5) # Give it time to boot
    
    health = test_health()
    if not health:
        sys.exit(1)
        
    pred = test_prediction()
    if not pred:
        sys.exit(1)
        
    print("All tests passed!")
