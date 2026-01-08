import os
import logging
from gpt4all import GPT4All

# Setup logging
logger = logging.getLogger(__name__)

# Config
MODEL_NAME = "Phi-3-mini-4k-instruct.Q4_0.gguf"
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
            # Attempt to use GPU (Vulkan) if available, otherwise CPU
            _model_instance = GPT4All(MODEL_NAME, model_path=MODEL_PATH, allow_download=True, device='gpu')
            logger.info("Model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise e
    return _model_instance

def local_generate(prompt: str, system_prompt: str = None, max_tokens: int = 512, temperature: float = 0.4) -> str:
    """
    Generates text using the local LLM.
    """
    model = get_model()
    
    # Construct prompt for Phi-3 Instruct format:
    # <|system|>\n{system_prompt}<|end|>\n<|user|>\n{prompt}<|end|>\n<|assistant|>\n
    
    formatted_prompt = ""
    if system_prompt:
        formatted_prompt += f"<|system|>\n{system_prompt}<|end|>\n"
    formatted_prompt += f"<|user|>\n{prompt}<|end|>\n<|assistant|>\n"

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
