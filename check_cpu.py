from gpt4all import GPT4All
import sys

try:
    print("Attempting to load model...")
    # device='cpu' forces CPU usage, potentially avoiding CUDA probing noise if supported, 
    # though GPT4All python bindings often auto-detect.
    model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf", allow_download=False)
    print("Model loaded successfully!")
    
    print("Generating test response...")
    response = model.generate("Say hello!", max_tokens=10)
    print(f"Response: {response}")
    print("SUCCESS: CPU Inference verified.")
except Exception as e:
    print(f"FAILURE: {e}")
    sys.exit(1)
