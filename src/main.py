from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-70b-chat")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-70b-chat")
