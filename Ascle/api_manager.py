import requests
import google.generativeai as genai
from anthropic import Anthropic
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline


class APIManager:
    def __init__(self, model_manager):
        self.model_manager = model_manager
        self.llama_pipeline = None  # Pipeline for LLaMA
        self.tokenizer = None  # Tokenizer for LLaMA

    def configure_gemini(self):
        genai.configure(api_key=self.model_manager.get_api_key('Gemini'))
        
    def configure_llama(self):
        """Configure LLaMA model from HuggingFace."""
        if self.llama_pipeline is None:
            self.tokenizer = AutoTokenizer.from_pretrained("huggingface/llama-model")
            model = AutoModelForCausalLM.from_pretrained("huggingface/llama-model")
            self.llama_pipeline = pipeline("text-generation", model=model, tokenizer=self.tokenizer)


    def call_chatgpt_api(self, text):
        headers = {
            "Authorization": f"Bearer {self.model_manager.get_api_key('ChatGPT')}",
            "Content-Type": "application/json"
        }
        payload = {"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": text}]}
        chatgpt_api_url = "https://api.openai.com/v1/chat/completions"
        response = requests.post(chatgpt_api_url, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        return f"ChatGPT API error: {response.status_code} - {response.text}"

    def call_claude_api(self, text):
        try:
            # Crear cliente de Anthropic y llamar al modelo Claude 3.5 Sonnet usando la Messages API
            claude = Anthropic(api_key=self.model_manager.get_api_key('Claude'))

            # Formatear el mensaje para la Messages API
            response = claude.messages.create(
                model="claude-3-5-sonnet-20240620",  # Modelo de Claude 3.5 Sonnet
                max_tokens=1024,  # Número máximo de tokens
                messages=[
                    {"role": "user", "content": text}  # Enviar el mensaje con rol "user"
                ]
            )
            
            # Extraer el texto de la respuesta
            if response.content and len(response.content) > 0:
                return response.content[0].text  # Acceder al primer bloque de texto
            else:
                return "No content found in response"
        except Exception as e:
            return f"Claude API call failed: {str(e)}"

    def call_gemini_api(self, text):
        try:
            # Configura tu clave de API
            self.configure_gemini()

            # Llamada a la API usando el modelo 'gemini-1.5-flash'
            model = genai.GenerativeModel("gemini-1.5-pro")
            response = model.generate_content(text)

            # Acceder al texto generado en la respuesta
            generated_text = response.candidates[0].content.parts[0].text
            return generated_text
        except Exception as e:
            return f"Gemini API error: {str(e)}"
        
        
    def call_llama_api(self, prompt):
        """Process the prompt using the LLaMA model."""
        try:
            self.configure_llama()
            response = self.llama_pipeline(prompt)[0]['generated_text']
            return response
        except Exception as e:
            return f"LLaMA API error: {str(e)}"


