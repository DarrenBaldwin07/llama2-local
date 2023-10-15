import json
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import subprocess
from fastapi import FastAPI
from fastapi.logger import logger
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

access_token = "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"
model_name = "meta-llama/Llama-2-13b-chat-hf"

class PromptBody(BaseModel):
    prompt: str

# Auth with huggingface before downloading llama2 (its a private model)
def hf_login():
    """
    Login to HuggingFace to access private models.
    """
    try:
        subprocess.run(["huggingface-cli", "login", "--token", access_token])
    except Exception as e:
        print(f"An error occurred while logging in: {e}")
    pass

hf_login()

tokenizer = AutoTokenizer.from_pretrained(model_name, token=access_token)

llama_pipeline = pipeline(
    "text-generation",
    model=model_name,
    torch_dtype=torch.float16,
    device_map="auto",
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def inference(prompt: str) -> str:
    print('> Running inference...')
    """
    Generate a response from the Llama model.

    Parameters:
        prompt (str): Your input/question for the model.

    Returns:
        None: Prints the model's response.
    """
    sequences = llama_pipeline(
        prompt,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        max_length=256,
    )
    print("Chatbot:", sequences[0]['generated_text'])
    return sequences[0]['generated_text']

@app.post("/predict")
def predict(body: PromptBody):
    res = inference(body.prompt)
    return {"response": json.dumps(res)}

@app.get("/health")
def health():
    return "ok"


def check_cuda_support():
    """
    Function to check if PyTorch can use CUDA GPUs.
    """
    return torch.cuda.is_available()


@app.get("/check_cuda_support")
async def get_cuda_support():
    """
    FastAPI endpoint to check if PyTorch can use CUDA GPUs.
    """
    cuda_support = check_cuda_support()
    return {"can_use_cuda": cuda_support}

# For shutting down the model at any point (feel free to remove this if un-needed)
@app.on_event("shutdown")
def shutdown_event():
    # Shutdown the model and perform any required cleanup here...
    logger.info("Shutting down model...")
    global model
    del model
    torch.cuda.empty_cache()
    logger.info("Model shutdown complete.")


# Only use this when in development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
