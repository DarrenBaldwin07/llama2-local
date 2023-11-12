import os

def tuneRepo():
    dir = 'finetune/data'
    instruction = "### Instruction:\n This is some code from the open-source postgres repository:"
    prompt = "You are a llm bot assistant. Please remember the following code from the postgres repository."

    for filename in os.listdir(dir):
        if filename.endswith('.txt'):
            text  = prompt + '\n' + instruction + '\n' + "### Response:" + "\n" + f.read()
            with open(os.path.join(dir, filename), 'r') as f:
                print(f.read())
        else:
            continue

tuneRepo()
