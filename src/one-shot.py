from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import subprocess

print("<<<< RUNNING LLAMA2 >>>>")

access_token = "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"
model_name = "meta-llama/Llama-2-13b-chat-hf"

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


def get_llama_response(prompt: str) -> None:
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



prompt = 'What is 1 + 1?'
get_llama_response(prompt)
