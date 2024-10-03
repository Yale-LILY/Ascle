from model_manager import ModelManager
from api_manager import APIManager
from command_processor import CommandProcessor
from Ascle import Ascle  # Import the Ascle class directly
import warnings

class AscleInterface:
    def __init__(self):
        """
        Initializes AscleInterface with the ModelManager, APIManager, Ascle, 
        and CommandProcessor for analyzing user input and processing actions.
        """
        
        # Suppress NVML initialization warnings
        warnings.filterwarnings("ignore", message="Can't initialize NVML")

        # Initialize ModelManager, Ascle, CommandProcessor, and APIManager
        self.model_manager = ModelManager()
        self.ascle = Ascle()  # Ascle handles medical terminology and tasks
        self.command_processor = CommandProcessor(self.model_manager)
        self.api_manager = APIManager(self.model_manager)  # APIManager handles API interactions
        self.using_ascle_model = False  # Tracks if Ascle model is in use
        self.model = None  # To store the selected model
    
    def choose_model(self, 
                     model, 
                     model_gpt=None, 
                     model_gemini=None, 
                     model_claude=None, 
                     model_llama=None, 
                     model_ascle=None):
        """
        Choose the primary model and update its version if provided. 
        If no version is provided, default versions are used.

        Parameters:
        model (str): The primary model to use (e.g., 'gpt', 'gemini', 'claude', 'llama', 'ascle').
        model_gpt (str, optional): Specific version of GPT, if provided.
        model_gemini (str, optional): Specific version of Gemini, if provided.
        model_claude (str, optional): Specific version of Claude, if provided.
        model_llama (str, optional): Specific version of LLaMA, if provided.
        model_ascle (str, optional): Specific version of Ascle, handled internally.
        """

        # Check which model is selected and set it up accordingly
        if model == 'gpt':
            self.model = model
            version = model_gpt or self.model_manager.get_default_version('gpt')
            self.model_manager.choose_model('gpt', version)
        elif model == 'gemini':
            self.model = model
            version = model_gemini or self.model_manager.get_default_version('gemini')
            self.model_manager.choose_model('gemini', version)
        elif model == 'claude':
            self.model = model
            version = model_claude or self.model_manager.get_default_version('claude')
            self.model_manager.choose_model('claude', version)
        elif model == 'llama':
            self.model = model
            version = model_llama or self.model_manager.get_default_version('llama')
            self.model_manager.choose_model('llama', version)
        elif model == 'ascle':
            # For Ascle, versions are handled internally within the Ascle class
            self.using_ascle_model = True
            if model_ascle:
                # Update the Ascle model version as needed
                self.ascle.update_scispacy_model(model_ascle)  # Update to a specific Ascle model
        else:
            raise ValueError(f"Invalid model input: {model}. Please select a valid model.")

    def process_prompt(self, prompt):
        """
        Process the input prompt based on the selected model (Ascle or other open models).

        Parameters:
        prompt (str): The user's input to be processed.

        Returns:
        str: The processed output from the appropriate model or function.
        """
        if self.using_ascle_model:
            # For Ascle models, determine the action (summarize, translate, etc.)
            action = self.command_processor.identify_action(prompt)
            return self._process_ascle_prompt(action, prompt)
        else:
            # For open models (GPT, Claude, etc.), delegate processing to the appropriate API
            return self._process_open_model_prompt(prompt)
    
    def _process_ascle_prompt(self, action, prompt, model_ascle=None):
        """
        Process a prompt using Ascle models based on the identified action.

        Parameters:
        action (str): The identified action (e.g., summarize, translate, QA).
        prompt (str): The text to be processed.
        model_ascle (str, optional): A specific fine-tuned model to use for Ascle, if provided.

        Returns:
        str: The result of the action performed by the Ascle model.
        """

        # Update Ascle models if a specific model is provided
        if model_ascle:
            if action in ['multi_choice_qa']:
                # Update the model for multi-choice QA
                self.ascle.update_bert_model(model_ascle)  # Example: PubMedBERT fine-tuned for HEADQA
            elif action in ['simplify_text', 'summarize']:
                # Update the model for text simplification or summarization
                self.ascle.update_scispacy_model(model_ascle)  # Example: BART fine-tuned for eLife
            elif action in ['translate']:
                # Update the model for automatic translation
                self.ascle.update_marian_model(model_ascle)  # Example: mT5 fine-tuned for en_es translation

        self.ascle.update_and_delete_main_record(prompt)  # Update the main record with the prompt

        # Process the identified action
        if action == 'summarize' or action == 'simplify_text':
            # Call get_layman_text with or without model_ascle based on availability
            if model_ascle:
                return self.ascle.get_layman_text(model_name=model_ascle)
            else:
                return self.ascle.get_layman_text()  # Use the default model
        elif action == 'translate':
            # Handle translation action
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
        elif action == 'question_generation' or action == 'multi_choice_qa':
            # Call get_question with or without model_ascle based on availability
            if model_ascle:
                return self.ascle.get_question(model_name=model_ascle)
            else:
                return self.ascle.get_question()  # Use the default model
        elif action == 'similar_documents':
            query_note, candidate_notes = self.command_processor.extract_text_for_similarity(prompt)
            return self.ascle.get_similar_documents()
        else:
            return "Ascle model action not recognized."

    def _process_open_model_prompt(self, prompt):
        """
        Process a prompt using open models (GPT, Claude, Gemini, etc.).

        Parameters:
        prompt (str): The text to be processed.

        Returns:
        str: The result from the selected open model.
        """
        # Get the selected model and its version
        selected_model = self.model_manager.get_selected_model()  
        print("Selected model:", selected_model)

        # Check which model is selected and call the corresponding API
        if self.model == 'gpt':
            return self.api_manager.call_chatgpt_api(prompt, selected_model)
        elif self.model == 'claude':
            return self.api_manager.call_claude_api(prompt, selected_model)
        elif self.model == 'gemini':
            return self.api_manager.call_gemini_api(prompt, selected_model)
        elif self.model == 'llama':
            return self.api_manager.call_llama_api(prompt, selected_model)
        else:
            return "No valid open model selected."

    def is_language_supported(self, language):
        """
        Check if the given language is supported by the translation system.

        Parameters:
        language (str): The target language.

        Returns:
        bool: True if the language is supported, False otherwise.
        """
        # Get the list of supported languages from Ascle
        supported_languages = self.ascle.get_supported_translation_languages()
        return language in supported_languages
