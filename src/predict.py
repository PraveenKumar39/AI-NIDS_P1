import pandas as pd
import numpy as np
import joblib
import os
import yaml
import logging

# Configure Structured Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("NIDSPredictor")

class NIDSPredictor:
    def __init__(self, model_path="models/rf_model.pkl", config_path="config/risk_rules.yaml", data_path="data/processed/train_encoded.csv"):
        self.model_path = model_path
        self.config_path = config_path
        self.data_path = data_path
        self.model = None
        self.feature_columns = None
        self.config = {}
        
        # Label mapping (based on previous encoding)
        # 0: BENIGN, 1: DDoS, 2: PortScan
        self.label_map = {0: "BENIGN", 1: "DDoS", 2: "PortScan"}
        
        self.load_config()
        self.load_model()
        self.load_features()

    def load_config(self):
        """Loads risk scoring configuration from YAML."""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    self.config = yaml.safe_load(f)
                logger.info(f"Configuration loaded from {self.config_path}")
            else:
                logger.warning(f"Config file {self.config_path} not found. Using defaults.")
                self.config = {}
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            self.config = {}

    def load_model(self):
        """Loads the trained RandomForest model."""
        try:
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
                logger.info(f"Model loaded from {self.model_path}")
            else:
                logger.error(f"Model file {self.model_path} not found.")
                self.model = None
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            self.model = None

    def load_features(self):
        """Loads feature names to ensure input data matches training data."""
        try:
            if os.path.exists(self.data_path):
                df = pd.read_csv(self.data_path, nrows=1)
                # Drop label columns to get feature list
                cols = [c for c in df.columns if c not in ['Label', 'Label_Encoded']]
                self.feature_columns = cols
            else:
                logger.warning(f"Training data not found at {self.data_path}. Feature verification disabled.")
        except Exception as e:
            logger.error(f"Error loading features: {e}")

    def calculate_risk_and_severity(self, label_idx, probability):
        """
        Maps predicted class and probability to Risk Score and Severity using loaded config.
        """
        label_name = self.label_map.get(label_idx, "Unknown")
        
        # Get rules from config or fall back to defaults
        rules = self.config.get('risk_mapping', {}).get(label_name, self.config.get('default', {}))
        
        base_risk = rules.get('base_risk', 50)
        max_risk = rules.get('max_risk', 50)
        
        # Calculate Risk
        risk_score = base_risk + (probability * (max_risk - base_risk))
        risk_score = min(risk_score, 100) # Cap at 100
        risk_score = int(risk_score)
        
        # Determine Severity from config if specific overrides exist, otherwise standard logic
        if 'severity' in rules:
            severity = rules['severity']
        else:
            # Fallback dynamic severity based on score
            if risk_score <= 20:
                severity = "Safe"
            elif risk_score <= 50:
                severity = "Medium"
            elif risk_score <= 80:
                severity = "High"
            else:
                severity = "Critical"
            
        return risk_score, severity, label_name

    def predict(self, input_data):
        """
        Predicts the class and risk for a given input.
        
        Args:
            input_data: DataFrame or dict containing feature values.
            
        Returns:
            List of dictionaries containing prediction results.
        """
        if self.model is None:
            logger.error("Attempted prediction with no model loaded.")
            return {"error": "Model not loaded"}

        # Convert dict to DataFrame if necessary
        if isinstance(input_data, dict):
            input_data = pd.DataFrame([input_data])
        elif hasattr(input_data, 'dict'): # Handle Pydantic models
             input_data = pd.DataFrame([input_data.dict(by_alias=True)])

        # Align features
        if self.feature_columns:
            # Add missing columns with 0
            for col in self.feature_columns:
                if col not in input_data.columns:
                    input_data[col] = 0
            # Reorder and select only training columns
            input_data = input_data[self.feature_columns]

        # Predict
        try:
            predictions = self.model.predict(input_data)
            probs = self.model.predict_proba(input_data)
            
            results = []
            for i, pred in enumerate(predictions):
                # Probability of the predicted class
                prob = probs[i][pred]
                
                risk_score, severity, label_name = self.calculate_risk_and_severity(pred, prob)
                
                result = {
                    "Attack Prediction": label_name,
                    "Confidence": round(prob, 4),
                    "Risk Score": risk_score,
                    "Severity": severity
                }
                logger.info(f"Prediction: {label_name}, Risk: {risk_score}, Severity: {severity}")
                results.append(result)
                
            return results
            
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            return {"error": str(e)}

if __name__ == "__main__":
    # Test
    predictor = NIDSPredictor()
    
    # Create a dummy row
    try:
        logging.info("Starting test run...")
        df_test = pd.DataFrame([{
            'Destination Port': 80,
            'Flow Duration': 1000,
            'Total Fwd Packets': 10
        }])
        
        results = predictor.predict(df_test)
        print(results)
            
    except Exception as e:
        print(f"Test failed: {e}")
