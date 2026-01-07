from backend.local_ai_engine import local_generate
import time

print("Starting short generation test...")
start = time.time()
response = local_generate("What is 2+2?", system_prompt="Answer briefly.", max_tokens=50)
end = time.time()
print(f"Time taken: {end - start:.2f}s")
print(f"Response: {response}")
