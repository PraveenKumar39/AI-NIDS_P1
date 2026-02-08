from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
from src.predict import NIDSPredictor
from src.schemas import NetworkFlow, PredictionResponse
import time
import logging
import os

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("API")

app = FastAPI(
    title="AI-NIDS API",
    version="1.0.0",
    description="Production-ready Network Intrusion Detection System API"
)

# Security
API_KEY_NAME = "X-API-Key"
API_KEY = os.getenv("NIDS_API_KEY", "secret-key-123") # Default for demo
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

# Global Predictor
predictor = None

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header != API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials"
        )
    return api_key_header

@app.on_event("startup")
async def load_model():
    global predictor
    logger.info("Loading NIDS model...")
    predictor = NIDSPredictor()
    if predictor.model is None:
        logger.error("Failed to load model on startup.")
    else:
        logger.info("Model loaded successfully.")

@app.get("/health")
def health_check():
    if predictor and predictor.model:
        return {"status": "healthy", "model_loaded": True}
    return {"status": "unhealthy", "model_loaded": False}

@app.post("/v1/predict", response_model=PredictionResponse, dependencies=[Depends(get_api_key)])
def predict(flow: NetworkFlow):
    """
    Predicts the risk and attack type for a given network flow.
    Requires 'X-API-Key' header.
    """
    if not predictor or not predictor.model:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    start_time = time.time()
    
    # Convert Pydantic model to dict
    input_data = flow.dict(by_alias=True)
    
    # Predict
    results = predictor.predict(input_data)
    
    if isinstance(results, dict) and "error" in results:
        raise HTTPException(status_code=500, detail=results["error"])
    
    # We expect a single result for a single input
    result = results[0]
    
    processing_time = (time.time() - start_time) * 1000
    
    response = PredictionResponse(
        prediction=result["Attack Prediction"],
        confidence=result["Confidence"],
        risk_score=result["Risk Score"],
        severity=result["Severity"],
        processing_time_ms=round(processing_time, 2)
    )
    
    logger.info(f"Processed flow from {flow.src_ip} -> {flow.dst_ip}: {response.prediction} (Risk: {response.risk_score})")
    
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api:app", host="0.0.0.0", port=8000, reload=True)
