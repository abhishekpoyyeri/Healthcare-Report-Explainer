from backend.extractor import extract_findings
from backend.formatter import generate_patient_mode, generate_clinician_mode
from backend.knowledge_base import map_to_citations
import asyncio

async def run_pipeline(report_text: str) -> dict:
    """
    Orchestrates the full AI pipeline:
    1. Extract findings
    2. Generate Patient & Clinician explanations
    3. Collect Citations
    4. Return structured JSON
    """
    
    # Step 1: Extract Findings
    findings_data = await extract_findings(report_text)
    
    # Step 2: Generate Explanations (Parallel)
    patient_task = generate_patient_mode(findings_data)
    clinician_task = generate_clinician_mode(findings_data)
    
    patient_explanation, clinician_explanation = await asyncio.gather(patient_task, clinician_task)
    
    # Step 3: Collect Citations
    # Scan findings and extract relevant terms for citation
    found_citations = []
    seen_urls = set()
    
    # Simple strategy: Scan keywords in the extracted 'findings' list or keys
    # Flatten findings to a string for simpler search, or iterate over specific keys
    search_text = str(findings_data.get("findings", "")) + " " + \
                  str(findings_data.get("critical_values", "")) + " " + \
                  str(findings_data.get("test_type", ""))
                  
    # This is a basic keyword match against our KB keys
    from backend.knowledge_base import KNOWLEDGE_BASE
    for term in KNOWLEDGE_BASE.keys():
        if term in search_text.lower():
            citation = KNOWLEDGE_BASE[term]
            if citation['url'] not in seen_urls:
                found_citations.append(citation['url'])
                seen_urls.add(citation['url'])
    
    # Step 4: Construct Final Response
    return {
        "patient_explanation": patient_explanation,
        "clinician_explanation": clinician_explanation,
        "citations": found_citations,
        "disclaimer": "This is an AI-generated explanation and does NOT constitute a medical diagnosis. Always consult a qualified physician for medical advice."
    }
