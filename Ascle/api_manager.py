# api_manager.py

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
        
        
    def configure_gemini(self):
        genai.configure(api_key=self.model_manager.get_api_key('Gemini'))
        
    def configure_llama(self,model):
        
        """Configure LLaMA model from HuggingFace."""
        token = self.model_manager.get_api_key("LLaMA")
        #token = "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"
        print("token llama:", token)
        if token:
            # Autenticar la sesión en Hugging Face usando el token
            login(token=token, add_to_git_credential=True)
        else:
            raise EnvironmentError("Hugging Face token (HF_TOKEN) not found. Please set it in the .env file.")

        llama_model= None
        
        if self.llama_pipeline is None:
            print("model llama:", model)
            if token:
                self.tokenizer = AutoTokenizer.from_pretrained(model)
                llama_model = AutoModelForCausalLM.from_pretrained(model)
            else:
                raise EnvironmentError("Hugging Face token (HF_TOKEN) not found. Please set it in the .env file.")
            
            #self.llama_pipeline = pipeline("text-generation", model=llama_model, tokenizer=self.tokenizer)
            self.llama_pipeline  = pipeline("text-generation", model=llama_model,  tokenizer=self.tokenizer)

        
        
    def call_chatgpt_api(self, text, model):
        #print("model chatgpt:", model, type(model))
        
        
        headers = {
            "Authorization": f"Bearer {self.model_manager.get_api_key('ChatGPT')}",
            "Content-Type": "application/json"
        }
        payload = {"model": model, "messages": [{"role": "user", "content": text}]}
        chatgpt_api_url = "https://api.openai.com/v1/chat/completions"
        response = requests.post(chatgpt_api_url, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        return f"ChatGPT API error: {response.status_code} - {response.text}"

    def call_claude_api(self, text, model):
        try:
            # Crear cliente de Anthropic
            claude = Anthropic(api_key=self.model_manager.get_api_key('Claude'))

            # Lista de modelos que utilizan la Completions API
            completions_models = ["claude-1.0", "claude-1.2", "claude-1.3"]

            # Determinar si el modelo utiliza la Completions API o la Messages API
            if model in completions_models:
                #print("Old model")
                # Utilizar la Completions API
                prompt = f"\n\nHuman: {text}\n\nAssistant:"
                response = claude.completions.create(
                    model=model,
                    max_tokens_to_sample=1024,
                    prompt=prompt,
                    stop_sequences=["\n\nHuman:"],
                )
                # Imprimir la respuesta de la API
                #print("Respuesta de la API:", response)
                # Extraer el texto de la respuesta
                if response and response.completion:
                    result_text = response.completion.strip()
                else:
                    return "No se encontró contenido en la respuesta"
            else:
                #print("New model")
                # Utilizar la Messages API
                response = claude.messages.create(
                    model=model,
                    max_tokens=1024,
                    messages=[
                        {"role": "user", "content": text}
                    ]
                )
                # Imprimir la respuesta de la API
                #print("Respuesta de la API:", response)
                # Extraer el texto de la respuesta
                if response.content and len(response.content) > 0:
                    result_text = response.content[0].text.strip()
                else:
                    return "No se encontró contenido en la respuesta"

            # Aquí agregamos el código para extraer el texto después de "Summary:"
            summary_index = result_text.find('Summary:')
            if summary_index != -1:
                # Extraer el texto que viene después de "Summary:"
                extracted_text = result_text[summary_index + len('Summary:'):].strip()
                return extracted_text
            else:
                # Si no se encuentra "Summary:", retornamos todo el texto
                return result_text

        except Exception as e:
            return f"La llamada a la API de Claude falló: {str(e)}"



    def call_gemini_api(self, text,model):
        try:
            # Configura tu clave de API
            self.configure_gemini()

            # Llamada a la API usando el modelo 'gemini-1.5-flash'
            model = genai.GenerativeModel(model)
            response = model.generate_content(text)

            # Acceder al texto generado en la respuesta
            generated_text = response.candidates[0].content.parts[0].text
            return generated_text
        except Exception as e:
            return f"Gemini API error: {str(e)}"

    def call_llama_api(self, text, model):
        """
        Process the prompt using the LLaMA model pipeline.
        """
        if self.llama_pipeline is None:
            self.configure_llama(model)

        # Generar el texto usando el pipeline configurado
        generated_text = self.llama_pipeline(text, max_new_tokens=500, early_stopping=True, do_sample=False, temperature=0.7 )
        #print("generated_text: ", generated_text)
        return generated_text[0]["generated_text"]
