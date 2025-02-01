from clemcore.backends import load_model_registry, get_model_for

# load the model registry:
load_model_registry()

api_models = ["gpt-4o-2024-11-20-openrouter",
              "claude-3-5-sonnet-2024-10-22-openrouter",
              "qwen-2.5-72B-Instruct-openrouter",
              "llama-3.1-8b-openrouter"]

local_models = ["ruadapt-llama3-8b",
                "saiga-llama3-8b",
                "Vikhr-Nemo-12B",
                "aya-expanse-8b",
                "TowerInstruct-13B-v0.1"]

# model name of the model to be loaded:
# model_name = "llama-3.1-8b-instant-Groq"
for model_name in local_models:
    # load the model, as a Model subclass instance:
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