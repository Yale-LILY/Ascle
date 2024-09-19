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

    def __init__(self, model_manager,history):
        """
        Initializes the APIManager with an instance of the ModelManager class.
        
        Parameters:
        model_manager (ModelManager): An instance of the ModelManager class.
        """
        self.model_manager = model_manager
        # Retrieve the Gemini API key from the ModelManager
        
        self.history = history  # Reference to the conversation history
        #self.configure_gemini()

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
        # Include conversation history in the payload
        messages = [{"role": "user", "content": entry['message']} if entry['role'] == 'user' else {"role": "assistant", "content": entry['message']} for entry in self.history]
        messages.append({"role": "user", "content": text})
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": messages
        }
        chatgpt_api_url = "https://api.openai.com/v1/chat/completions"

        response = requests.post(chatgpt_api_url, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            print(f"{Fore.CYAN}ChatGPT response: {result['choices'][0]['message']['content']}")
            chatgpt_response = result['choices'][0]['message']['content']
            return chatgpt_response
        else:
            print(f"{Fore.RED}ChatGPT API error: {response.status_code} - {response.text}")
            error_message = f"ChatGPT API error: {response.status_code} - {response.text}"
            return error_message
        
    def call_claude_api(self, text):
        """
        Calls the Claude API to process the provided text with conversation history.
        
        Parameters:
        text (str): The text to process.
        
        Returns:
        str: The response from Claude.
        """
        try:
            # Create the conversation prompt from self.history
            conversation_prompt = ""
            for entry in self.history:
                if entry['role'] == 'user':
                    conversation_prompt += f"User: {entry['message']}\n"
                else:
                    conversation_prompt += f"Assistant: {entry['message']}\n"

            # Add the current user input to the conversation
            conversation_prompt += f"User: {text}\nAssistant:"

            # Initialize the Anthropic instance
            claude = Anthropic(api_key=self.model_manager.get_api_key('Claude'))
            
            # Make the API call with the full conversation prompt
            response = claude.completions.create(
                model="claude-3",
                prompt=conversation_prompt,
                max_tokens_to_sample=1024
            )
            print(f"{Fore.CYAN}Claude response: {response.completion}")
            return response.completion

        except Exception as e:
            error_message = f"Claude API call failed: {str(e)}"
            print(f"{Fore.RED}{error_message}")
            return error_message

    def call_gemini_api(self, text):
        """
        Calls the Gemini API to process the provided text with conversation history.
        
        Parameters:
        text (str): The text to process.
        
        Returns:
        str: The response from Gemini.
        """
        try:
            self.configure_gemini()
            # Create the conversation prompt from self.history
            conversation_prompt = ""
            for entry in self.history:
                if entry['role'] == 'user':
                    conversation_prompt += f"User: {entry['message']}\n"
                else:
                    conversation_prompt += f"Assistant: {entry['message']}\n"

            # Add the current user input to the conversation without "Assistant:"
            #conversation_prompt += f"User: {text}\n"

            # Initialize the model
            model = genai.GenerativeModel(model_name="gemini-1.5-pro")
            # Make the API call with the full conversation prompt
            response = model.generate_content(conversation_prompt)
            print(f"{Fore.CYAN}Gemini 1.5 response: {response.text}")
            return response.text

        except Exception as e:
            error_message = f"Gemini API error: {str(e)}"
            print(f"{Fore.RED}{error_message}")
            return error_message


