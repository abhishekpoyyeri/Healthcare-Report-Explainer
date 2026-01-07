import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import os
from dotenv import load_dotenv

from backend.models import AnalysisResponse
from backend.pipeline import run_pipeline
# Ensure model is expected to load on startup or first request
from backend.local_ai_engine import get_model

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI(title="Medical Report Explainer AI (Local)")

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.on_event("startup")
async def startup_event():
    # Preload model on startup to avoid delay on first request
    try:
        get_model()
        logger.info("Local AI Engine initialized.")
    except Exception as e:
        logger.error(f"Failed to initialize Local AI Engine: {e}")

@app.get("/")
def read_root():
    # Serve index.html at root
    return FileResponse("frontend/index.html")

class ReportInput(BaseModel):
    report_text: str

@app.post("/explain-report", response_model=AnalysisResponse)
async def explain_report(request: ReportInput):
    report_text = request.report_text
    
    logger.info("Received report for analysis")

    if not report_text.strip():
        logger.warning("Empty report text received")
        raise HTTPException(status_code=400, detail="Empty report content")
    
    # Removed OPENAI_API_KEY check as we are using Local LLM

    try:
        # Use new pipeline
        analysis_result = await run_pipeline(report_text)
        logger.info("Report analysis completed successfully")
        return analysis_result
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI Processing Failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
