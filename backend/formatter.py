import json
from backend.local_ai_engine import local_generate

async def generate_patient_mode(data: dict) -> str:
    """
    Generates a patient-friendly explanation from the extracted data using Local LLM.
    """
    system_prompt = "You are a helpful medical assistant for patients."
    
    prompt = f"""
    Using the extracted report data below, explain the report in simple everyday language.

    Include these sections:
    - Overview of the test
    - What the report says (Findings)
    - Possible implications
    - Red flags to watch (if any)
    - Questions the patient should ask their doctor

    Keep language non-technical and reassuring.
    End with disclaimer: "This is not a diagnosis. Consult a qualified physician."

    Extracted Data:
    {json.dumps(data, indent=2)}
    """
    
    try:
        return local_generate(prompt, system_prompt=system_prompt)
    except Exception as e:
        return f"Error generating patient explanation: {str(e)}"

async def generate_clinician_mode(data: dict) -> str:
    """
    Generates a clinician-focused summary from the extracted data using Local LLM.
    """
    system_prompt = "You are a professional medical assistant for clinicians."
    
    prompt = f"""
    Summarize the extracted report data into a concise bullet-point professional overview.

    Must contain:
    - Key findings
    - Critical values
    - Impression in one line
    - Suggested next steps (non-prescriptive)

    Do NOT recommend medications or treatments.
    Limit to under 10 bullets.

    Extracted Data:
    {json.dumps(data, indent=2)}
    """

    try:
        return local_generate(prompt, system_prompt=system_prompt)
    except Exception as e:
        return f"Error generating clinician summary: {str(e)}"
