import os
import logging
from gpt4all import GPT4All

# Setup logging
logger = logging.getLogger(__name__)

# Config
MODEL_NAME = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"
# Allow overriding model path via env, default to current directory or standard cache
MODEL_PATH = os.getenv("LOCAL_MODEL_PATH", None) 

_model_instance = None

def get_model():
    """
    Singleton pattern to load the model once.
    """
    global _model_instance
    if _model_instance is None:
        logger.info(f"Loading Local LLM: {MODEL_NAME}...")
        try:
            # GPT4All will download the model to ~/.cache/gpt4all/ if not found
            _model_instance = GPT4All(MODEL_NAME, model_path=MODEL_PATH, allow_download=True)
            logger.info("Model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise e
    return _model_instance

def local_generate(prompt: str, system_prompt: str = None, max_tokens: int = 1000, temperature: float = 0.7) -> str:
    """
    Generates text using the local LLM.
    """
    model = get_model()
    
    # Construct prompt based on simple concatenation or chat template if supported
    # Llama 3 Instruct format:
    # <|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n
    
    formatted_prompt = "<|begin_of_text|>"
    if system_prompt:
        formatted_prompt += f"<|start_header_id|>system<|end_header_id|>\n\n{system_prompt}<|eot_id|>"
    formatted_prompt += f"<|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"

    try:
        output = model.generate(
            formatted_prompt, 
            max_tokens=max_tokens, 
            temp=temperature
        )
        return output
    except Exception as e:
        logger.error(f"Generation failed: {e}")
        return ""
