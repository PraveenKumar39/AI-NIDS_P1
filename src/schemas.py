from pydantic import BaseModel, Field
from typing import Optional, List

class NetworkFlow(BaseModel):
    """
    Represents a single network flow record with features required for prediction.
    Features should match those used in training. 
    Using a subset of critical features for validation examples, but allowing dynamic dict for full model compatibility.
    """
    # Essential identification (optional for prediction but good for logging)
    flow_id: Optional[str] = Field(None, alias="Flow ID")
    src_ip: Optional[str] = Field(None, alias="Source IP")
    dst_ip: Optional[str] = Field(None, alias="Destination IP")
    
    # We use extra="allow" to accept all other numerical features without defining 80+ fields manually here
    class Config:
        extra = "allow"

class PredictionResponse(BaseModel):
    """
    Standardized response format for the NIDS API.
    """
    prediction: str
    confidence: float
    risk_score: int
    severity: str
    processing_time_ms: float
