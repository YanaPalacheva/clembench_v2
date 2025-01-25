from clemcore.backends import load_model_registry, get_model_for

# load the model registry:
load_model_registry()

# model name of the model to be loaded:
# model_name = "llama-3.1-8b-instant-Groq"
model_name = "aya-expanse-8b"
# load the model, as a Model subclass instance (HuggingfaceLocalModel in this case):
model = get_model_for(model_name)
# set required generation arguments/sampling parameters:
model.set_gen_arg('temperature', 0.0)  # temperature 0.0 for deterministic sampling
model.set_gen_arg('max_tokens', 25)  # maximum number of generated tokens

# messages list:
messages = [
    {'role': "user", 'content': "Hello!"},
    {'role': "assistant", 'content': "Hello! How can I help you?"},
    {'role': "user", 'content': "Tell me the name of the capital of Australia."},
]

# generate a response:
prompt, response, response_text = model.generate_response(messages)
print(f"{model_name} reply:")
print(response_text)