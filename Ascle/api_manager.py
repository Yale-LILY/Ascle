# api_manager.py

import requests
from colorama import Fore
import google.generativeai as genai
from anthropic import Anthropic


class APIManager:
    """
    APIManager handles interactions with external APIs like ChatGPT, Claude, and Gemini.
    It provides methods to communicate with these APIs for various tasks.
    """

    def __init__(self, model_manager):
        """
        Initializes the APIManager with an instance of the ModelManager class.
        
        Parameters:
        model_manager (ModelManager): An instance of the ModelManager class.
        """
        self.model_manager = model_manager
        self.configure_gemini()

    def configure_gemini(self):
        """
        Configures the Gemini API with the provided API key.
        """
        genai.configure(api_key=self.model_manager.get_api_key('Gemini'))

    def call_chatgpt_api(self, text):
        """
        Calls the ChatGPT API to process the provided text.
        
        Parameters:
        text (str): The text to process.
        """
        headers = {
            "Authorization": f"Bearer {self.model_manager.get_api_key('ChatGPT')}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": text}]
        }
        chatgpt_api_url = "https://api.openai.com/v1/chat/completions"

        response = requests.post(chatgpt_api_url, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            print(f"{Fore.CYAN}ChatGPT response: {result['choices'][0]['message']['content']}")
        else:
            print(f"{Fore.RED}ChatGPT API error: {response.status_code} - {response.text}")

    def call_claude_api(self, text):
        """
        Calls the Claude API to process the provided text.
        
        Parameters:
        text (str): The text to process.
        """
        try:
            # Initialize the Anthropic instance
            claude = Anthropic(api_key=self.model_manager.get_api_key('Claude'))
            response = claude.completions.create(
                model="claude-3",
                prompt=text,
                max_tokens_to_sample=1024
            )
            print(f"{Fore.CYAN}Claude response: {response.completion}")
        except Exception as e:
            print(f"{Fore.RED}Claude API call failed: {str(e)}")

    def call_gemini_api(self, text):
        """
        Calls the Gemini API to process the provided text.
        
        Parameters:
        text (str): The text to process.
        """
        try:
            # Initialize the model
            model = genai.GenerativeModel(model_name="gemini-1.5-pro")
            response = model.generate_content(text)
            print(f"{Fore.CYAN}Gemini 1.5 response: {response.text}")
        except Exception as e:
            print(f"{Fore.RED}Gemini API error: {str(e)}")

