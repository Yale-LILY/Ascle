import os
from dotenv import load_dotenv

class ModelManager:
    def __init__(self, config_file=".env"):
        """
        Initializes the ModelManager and loads API keys from the specified configuration file.
        """
        load_dotenv(config_file)
        self.selected_model = None
        self.api_keys = {
            'ChatGPT': os.getenv("CHATGPT_API_KEY"),
            'Claude': os.getenv("CLAUDE_API_KEY"),
            'Gemini': os.getenv("GEMINI_API_KEY"),
            'LLaMA': os.getenv("HF_TOKEN")
        }
    
    def choose_model(self, model, model_version=None):
        """
        Select a model and its version based on user input or default version.
        """
        valid_models = ['gpt', 'claude', 'gemini', 'llama', 'ascle']
        if model in valid_models:
            self.selected_model = model_version or self.get_default_version(model)
            return True
        else:
            print(f"Invalid model choice: {model}. Valid options are {', '.join(valid_models)}.")
            return False
    
    def get_selected_model(self):
        return self.selected_model
    
    def get_default_version(self, model):
        """
        Define default versions for models if no specific version is provided.
        """
        default_versions = {
            'gpt': 'gpt-4',
            'claude': 'claude-1.3',
            'gemini': 'gemini-1.5-flash',
            'llama': 'meta-llama/Llama-2-7b-chat-hf',
            'ascle': None  # Ascle doesn't have versions in the ModelManager, handled internally
        }
        return default_versions.get(model, None)

    def get_api_key(self, model_name):
        """
        Returns the API key or token for the specified model if applicable.

        Parameters:
        model_name (str): The model for which to retrieve the API key (e.g., 'ChatGPT', 'Claude', 'Gemini', 'LLaMA').

        Returns:
        str: The API key or token if found, otherwise None.
        """
        return self.api_keys.get(model_name)