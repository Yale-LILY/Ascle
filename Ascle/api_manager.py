import requests
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from anthropic import Anthropic
import google.generativeai as genai
from huggingface_hub import login
import torch

class APIManager:
    def __init__(self, model_manager):
        self.model_manager = model_manager
        self.llama_pipeline = None  # Pipeline for LLaMA
        self.tokenizer = None

    def configure_api(self, model_name):
        """Generic API configuration based on model name"""
        api_key = self.model_manager.get_api_key(model_name)
        if model_name == 'gemini':
            genai.configure(api_key=api_key)
        elif model_name == 'llama':
            if api_key:
                login(token=api_key, add_to_git_credential=True)
            else:
                raise EnvironmentError(f"Token for {model_name} not found.")
        # Additional model configurations if needed

    def call_model_api(self, model_name, text, model):
        """Handle model-specific API calls using a single method."""
        if model_name == 'chatgpt':
            return self._call_chatgpt(text, model)
        elif model_name == 'claude':
            return self._call_claude(text, model)
        elif model_name == 'gemini':
            return self._call_gemini(text, model)
        elif model_name == 'llama':
            return self._call_llama(text, model)
        else:
            raise ValueError(f"Unsupported model: {model_name}")

    def _call_chatgpt(self, text, model):
        headers = {
            "Authorization": f"Bearer {self.model_manager.get_api_key('chatgpt')}",
            "Content-Type": "application/json"
        }
        payload = {"model": model, "messages": [{"role": "user", "content": text}]}
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        return f"Error: {response.status_code} - {response.text}"

    def _call_claude(self, text, model):
        claude = Anthropic(api_key=self.model_manager.get_api_key('claude'))
        prompt = f"\n\nHuman: {text}\n\nAssistant:"
        response = claude.completions.create(model=model, max_tokens_to_sample=1024, prompt=prompt, stop_sequences=["\n\nHuman:"])
        return response.completion.strip() if response and response.completion else "Error: No content found"

    def _call_gemini(self, text, model):
        self.configure_api('gemini')
        model = genai.GenerativeModel(model)
        response = model.generate_content(text)
        return response.candidates[0].content.parts[0].text

    def _call_llama(self, text, model):
        if self.llama_pipeline is None:
            self.configure_api('llama')
            self.tokenizer = AutoTokenizer.from_pretrained(model)
            llama_model = AutoModelForCausalLM.from_pretrained(model)
            self.llama_pipeline = pipeline("text-generation", model=llama_model, tokenizer=self.tokenizer)
        generated_text = self.llama_pipeline(text, max_new_tokens=500, early_stopping=True, do_sample=False, temperature=0.7)
        return generated_text[0]["generated_text"]
