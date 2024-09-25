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
            'Gemini': os.getenv("GEMINI_API_KEY")
        }
    
    def choose_model(self, model_number=None):
        if model_number == '1':
            self.selected_model = 'ChatGPT'
        elif model_number == '2':
            self.selected_model = 'Claude'
        elif model_number == '3':
            self.selected_model = 'Gemini'            
        elif model_number == '4':  # Assuming '4' is for LLaMA
            self.selected_model = 'LLaMA'
        else:
            return False
        return True
    
    def get_selected_model(self):
        return self.selected_model
    
    def get_api_key(self, model_name):
        return self.api_keys.get(model_name)
