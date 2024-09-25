from model_manager import ModelManager
from api_manager import APIManager
from command_processor import CommandProcessor
from Ascle import Ascle  # Import the Ascle class directly
import warnings

class AscleInterface:
    def __init__(self):
        """
        Initialize AscleInterface with the model manager, API manager, Ascle,
        and command processor for analyzing the user's input.
        """
        
        warnings.filterwarnings("ignore", message="Can't initialize NVML")

        self.model_manager = ModelManager()
        self.ascle = Ascle()  # Replacing medical_processor with Ascle
        self.command_processor = CommandProcessor(self.model_manager)
        self.api_manager = APIManager(self.model_manager)  # No need for history now
        self.using_ascle_model = False  # Variable to track if using ascle models

    def choose_model(self, model_type):
        """
        Choose between a ascle model or a specific open model like ChatGPT, Claude, or Gemini.

        Parameters:
        model_type (str): 'chatgpt', 'claude', 'gemini' for using external models,
                          'ascle' to use the internal models for medical text processing.
        """
        if model_type == 'Ascle':
            self.using_ascle_model = True  # Set to use ascle models
        elif model_type in ['chatgpt', 'claude', 'gemini', 'LLaMA']:
            self._choose_open_model(model_type)  # Set the open model based on user choice
            self.using_ascle_model = False  # Set to use external model
        else:
            raise ValueError("Invalid choice. Please select 'chatgpt', 'claude', 'gemini', 'LLaMA', or 'ascle'.")

    def _choose_open_model(self, model_name):
        """
        Set the open model to use based on the user selection (ChatGPT, Claude, Gemini or LLaMA).
        
        Parameters:
        model_name (str): The selected open model ('chatgpt', 'claude', 'gemini', 'LLaMA).
        """
        model_map = {'chatgpt': '1', 'claude': '2', 'gemini': '3'}
        model_number = model_map.get(model_name)
        self.model_manager.choose_model(model_number)

    def process_prompt(self, prompt):
        """
        Process the prompt based on the selected model (ascle or specific open model).

        Parameters:
        prompt (str): The user's input to be processed.

        Returns:
        str: The processed output from the appropriate model or function.
        """
        if self.using_ascle_model:
            # For ascle models, analyze the command to determine the action (summarize, translate, etc.)
            action = self.command_processor.identify_action(prompt)
            return self._process_ascle_prompt(action, prompt)
        else:
            # For open models, simply delegate the processing to the selected model
            return self._process_open_model_prompt(prompt)

    def _process_ascle_prompt(self, action, prompt):
        """
        Process a prompt using ascle models (Ascle) based on the identified action.

        Parameters:
        action (str): The identified action (e.g., summarize, translate).
        prompt (str): The text to process.

        Returns:
        str: The result of the action performed by the ascle model.
        """
        self.ascle.update_and_delete_main_record(prompt)  # Update the main record with the prompt

        if action == 'summarize':
            return self.ascle.get_single_record_summary()
        elif action == 'translate':
            target_language = self.command_processor.detect_language(prompt)
            if self.is_language_supported(target_language):
                return self.ascle.get_translation(target_language)
            else:
                return f"Error: The language '{target_language}' is not supported for translation."
        elif action == 'named_entities':
            return self.ascle.get_named_entities()
        elif action == 'linked_entities':
            return self.ascle.get_linked_entities()
        elif action == 'pos_tagging':
            return self.ascle.get_pos_tags()
        elif action == 'abbreviations':
            return self.ascle.get_abbreviations()
        elif action == 'hyponyms':
            return self.ascle.get_hyponyms()
        elif action == 'question_generation':
            return self.ascle.get_question()
        elif action == 'similar_documents':
            query_note, candidate_notes = self.command_processor.extract_text_for_similarity(prompt)
            return self.ascle.get_similar_documents()
        else:
            return "Ascle model action not recognized."

    def _process_open_model_prompt(self, prompt):
        """
        Process a prompt using open models (ChatGPT, Claude, Gemini).

        Parameters:
        prompt (str): The text to process.

        Returns:
        str: The result from the selected open model.
        """
        selected_model = self.model_manager.get_selected_model()
        if selected_model == 'ChatGPT':
            return self.api_manager.call_chatgpt_api(prompt)
        elif selected_model == 'Claude':
            return self.api_manager.call_claude_api(prompt)
        elif selected_model == 'Gemini':
            return self.api_manager.call_gemini_api(prompt)
        elif selected_model == 'LLaMA':
            return self.api_manager.call_llama_api(prompt)
        else:
            return "No valid open model selected."

    def is_language_supported(self, language):
        """
        Checks if the language is supported by the translation system.
        """
        supported_languages = self.ascle.get_supported_translation_languages()
        return language in supported_languages
