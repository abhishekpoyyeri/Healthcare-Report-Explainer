import os
from openai import AsyncOpenAI
import json
from backend.models import AnalysisResponse

# Initialize OpenAI client
# Ensure OPENAI_API_KEY is set in environment variables
aclient = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def analyze_medical_report(text: str) -> AnalysisResponse:
    prompt = f"""
    You are an expert medical AI assistant. Analyze the following medical report (radiology or lab report) and provide two distinct explanations:
    
    1. **Patient Mode**: Simple, clear language suitable for a layperson. Explain medical terms, valid ranges, and key takeaways. Avoid alarming language but be accurate.
    2. **Clinician Mode**: Technical, concise, using standard medical terminology. Focus on differential diagnoses, key findings, and action items.
    
    Also provide a list of 3 reliable public source citations (URLs) relevant to the findings, and a standard medical disclaimer.
    
    Return the result specifically as a JSON object with the following keys:
    - patient_explanation
    - clinician_explanation
    - citations (list of strings)
    - disclaimer
    
    Report Text:
    {text}
    """

    try:
        response = await aclient.chat.completions.create(
            model="gpt-4o", # Or gpt-3.5-turbo if preferred for cost
            messages=[
                {"role": "system", "content": "You are a helpful and accurate medical AI assistant. Always output JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        data = json.loads(content)
        
        return AnalysisResponse(**data)

    except Exception as e:
        # Fallback or error handling
        print(f"Error in AI analysis: {e}")
        raise e
