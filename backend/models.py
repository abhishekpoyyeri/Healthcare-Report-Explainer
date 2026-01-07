from pydantic import BaseModel
from typing import List, Optional

class AnalysisResponse(BaseModel):
    patient_explanation: str
    clinician_explanation: str
    citations: List[str]
    disclaimer: str
