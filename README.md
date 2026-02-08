# AI-NIDS

AI-based Intrusion Detection System using the CIC-IDS dataset.

## Deployment (Streamlit Cloud)

1.  **Push to GitHub**:
    -   Create a new repository on GitHub.
    -   Push this code to the main branch.

2.  **Deploy**:
    -   Go to [share.streamlit.io](https://share.streamlit.io/).
    -   Connect your GitHub account.
    -   Select your repository and the main file path: `app.py`.
    -   Click **Deploy**.

The application will install dependencies from `requirements.txt` and go live.

## Application Modes

### 1. Dashboard (Interactive UI)
Run the Streamlit app for a visual interface:
```bash
python -m streamlit run app.py
```

### 2. REST API (Headless Service)
Run the FastAPI production server (use one of the following):

**Option A: Using the helper script (Windows PowerShell)**
```powershell
.\start_api.bat
```

**Option B: Manually**
```bash
python -m uvicorn src.api:app --host 0.0.0.0 --port 8000
```

**Accessing the API:**
Once the server is running, open your **web browser** and go to:
-   **Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
-   **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

**Auth**: Requires header `X-API-Key: secret-key-123`.

### 3. Docker (Containerized)
Build and run the container:
```bash
docker build -t ai-nids .
docker run -p 8000:8000 ai-nids
```

## 🏗️ Architecture
The system follows a clean, modular pipeline:
- **`src/preprocess.py`**: ETL pipeline (Load -> Clean -> Encode -> Save).
- **`src/train.py`**: Trains **Random Forest**, **XGBoost**, and **Isolation Forest** models.
- **`src/evaluate.py`**: Generates advanced metrics (ROC-AUC, Feature Importance).
- **`src/realtime_detector.py`**: Simulates live traffic analysis with risk alerts.
- **`src/api.py`**: Production-Ready FastAPI backend.
- **`app.py`**: Streamlit Dashboard for visualization.

## 📊 Model Performance
We compared multiple models to select the best engine.

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Random Forest** | **0.96** | **0.96** | **0.96** | **0.96** | **0.99** |
| XGBoost | 0.94 | 0.94 | 0.94 | 0.94 | 0.98 |

*Note: Isolation Forest is used as a secondary anomaly detector for unknown attacks.*

### 🔍 Top Features (Explainability)
The model prioritizes these network features to detect attacks:
1.  **Packet Length Mean**
2.  **Flow Duration**
3.  **Total Fwd Packets**
4.  **Flow Bytes/s**
5.  **Fwd IAT Total**

## 📉 Visualizations
#### Confusion Matrix (Random Forest)
![Confusion Matrix](reports/confusion_matrix.png)

#### ROC Curve (Random Forest)
![ROC Curve](reports/roc_curve.png)

## 🛡️ False Positive Mitigation
To reduce false alarms in a production environment, we implement:
1.  **Threshold Tuning**: We only flag "Critical" alerts if the risk score > 80.
    -   *Current Setting*: `config/risk_rules.yaml` defines strict bands.
2.  **Feature Scaling**: Input data is standardized to prevent outliers from skewing predictions.
3.  **Human-in-the-Loop**: High-severity alerts are forwarded to the SOC (Security Operations Center) for manual verification.

## 🔮 Future Improvements
-   [ ] **Deep Learning**: Experiment with LSTM for sequence-based anomaly detection.
-   [ ] **Cloud Native**: Deploy on AWS/Azure with auto-scaling.
-   [ ] **SIEM Integration**: Forward logs to Splunk or ELK Stack.

