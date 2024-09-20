# model_manager.py

import os
from colorama import Fore
from dotenv import load_dotenv  # Importar load_dotenv para leer el archivo .env

class ModelManager:
    """
    ModelManager is responsible for managing and switching between different AI models.
    It also handles the setup of API keys.
    """
    
    def __init__(self, config_file=".env"):
        """
        Initializes the ModelManager and loads API keys from the specified configuration file.
        
        Parameters:
        config_file (str): Path to the configuration file containing the API keys.
        """
        # Load environment variables from the .env file
        load_dotenv(config_file)
        
        self.selected_model = None
        self.api_keys = {
            'ChatGPT': os.getenv("CHATGPT_API_KEY"),
            'Claude': os.getenv("CLAUDE_API_KEY"),
            'Gemini': os.getenv("GEMINI_API_KEY")
        }
        
    def choose_model(self, model_number=None):
        """
        Selects an AI model based on the model_number provided.
        
        Parameters:
        model_number (str): '1' for ChatGPT, '2' for Claude, '3' for Gemini.
        
        Returns:
        bool: True if a valid model was selected, False otherwise.
        """
        if model_number is not None:
            if model_number == '1':
                self.selected_model = 'ChatGPT'
            elif model_number == '2':
                self.selected_model = 'Claude'
            elif model_number == '3':
                self.selected_model = 'Gemini'
            else:
                print(f"{Fore.RED}Invalid choice. Please select 1, 2, or 3.")
                return False
            print(f"{Fore.CYAN}Switched to {self.selected_model} successfully.")
            return True
        else:
            # Fallback to interactive mode if no argument is provided
            print(f"{Fore.CYAN}Choose a model:")
            print(f"1. ChatGPT")
            print(f"2. Claude 3.5")
            print(f"3. Gemini 1.5")

            while True:
                choice = input(f"{Fore.GREEN}Enter the number of the model you want to use (1, 2, or 3):\n")
                if choice in ['1', '2', '3']:
                    return self.choose_model(choice)
                else:
                    print(f"{Fore.RED}Invalid choice. Please select 1, 2, or 3.")
            return True
    
    def get_selected_model(self):
        """
        Returns the currently selected model.
        
        Returns:
        str: The name of the selected model.
        """
        return self.selected_model
    
    def get_api_key(self, model_name):
        """
        Retrieves the API key for a given model.
        
        Parameters:
        model_name (str): The name of the model ('ChatGPT', 'Claude', or 'Gemini').
        
        Returns:
        str: The API key for the specified model.
        """
        api_key = self.api_keys.get(model_name)
        
        if not api_key:
            print(f"{Fore.RED}API key for {model_name} is not set. Please check your .env file.")
        return api_key
