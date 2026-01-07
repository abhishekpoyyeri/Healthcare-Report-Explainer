import json
import re
from backend.local_ai_engine import local_generate

async def extract_findings(report_text: str) -> dict:
    """
    Extracts structured findings from a medical report using Local LLM.
    """
    
    system_prompt = "You are a precise medical data extraction AI. Extract information strictly from the text provided. Output strictly valid JSON."
    
    prompt = f"""
    Task:
    Read the provided medical report text and extract ONLY explicitly stated information.
    Do not add diagnoses or hallucinations.

    Identify:
    - Test type
    - Body part or panel
    - Findings (list)
    - Impression
    - Critical values (list)

    Return STRICTLY in JSON format with this structure. Do not include markdown formatting like ```json.
    {{
    "test_type": "string",
    "body_part_or_panel": "string",
    "findings": ["string", "string"],
    "impression": "string",
    "critical_values": ["string"]
    }}

    Report Text:
    {report_text}
    """

    try:
        # Run local generation
        # Not async in GPT4All usually, but running inside async func is fine for now
        # Ideally would run in threadpool if high concurrency
        response_text = local_generate(prompt, system_prompt=system_prompt, temperature=0.1)
        
        # Cleanup potential markdown code blocks
        clean_text = response_text.replace("```json", "").replace("```", "").strip()
        
        # Attempt to find JSON start/end if there's extra chatter
        start_idx = clean_text.find("{")
        end_idx = clean_text.rfind("}")
        if start_idx != -1 and end_idx != -1:
            clean_text = clean_text[start_idx:end_idx+1]

        data = json.loads(clean_text)
        return data

    except Exception as e:
        print(f"Extraction Error: {e}")
        # Return partial/empty structure on error to prevent crash
        return {
            "test_type": "Unknown",
            "body_part_or_panel": "Unknown",
            "findings": [f"Error extracting data: {str(e)}"],
            "impression": "Extraction failed",
            "critical_values": []
        }
