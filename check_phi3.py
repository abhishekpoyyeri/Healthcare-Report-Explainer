import sys
import os

# Add current directory to path so we can import backend
sys.path.append(os.getcwd())

try:
    from backend.local_ai_engine import get_model, local_generate, MODEL_NAME
    
    print(f"Testing Model: {MODEL_NAME}")
    
    # Trigger model load
    model = get_model()
    print("Model loaded successfully.")
    
    # Test generation
    prompt = "Explain why the sky is blue in one sentence."
    print(f"Generating response for: '{prompt}'")
    
    response = local_generate(prompt)
    print(f"Response: {response}")
    
    if response and len(response) > 5:
        print("SUCCESS: Generation worked.")
    else:
        print("FAILURE: Response was empty or too short.")
        sys.exit(1)

except Exception as e:
    print(f"FAILURE: {e}")
    sys.exit(1)
