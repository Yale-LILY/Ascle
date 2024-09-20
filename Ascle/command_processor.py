import re
from transformers import pipeline
from api_manager import APIManager
from Ascle import Ascle  # Importar la clase Ascle para usar sus métodos directamente
import torch

class CommandProcessor:
    def __init__(self, model_manager):
        """
        Initializes the CommandProcessor with a ModelManager instance and sets up zero-shot classification.
        """
        self.device = 0 if torch.cuda.is_available() else -1
        self.model_manager = model_manager
        self.classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=self.device, clean_up_tokenization_spaces=True)
        self.api_manager = APIManager(model_manager)
        self.ascle = Ascle()  # Instanciar Ascle para usar sus métodos directamente

    def process_command(self, command):
        """
        Process the command by identifying the action and delegating the task accordingly.
        """
        action = self.identify_action(command)
        return self.delegate_command(action, command)

    def identify_action(self, command):
        """
        Identifies the action requested in the command using zero-shot classification.
        """
        return self.identify_action_with_zero_shot(command)

    def delegate_command(self, action, command):
        """
        Delegates the command to the appropriate function based on the identified action.
        """
        # Llamar directamente a los métodos de Ascle
        if action == 'summarize':
            return self.ascle.get_single_record_summary()
        elif action == 'translate':
            target_language = self.detect_language(command)
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
            query_note, candidate_notes = self.extract_text_for_similarity(command)
            return self.ascle.get_similar_documents()
        elif action == 'supported_translation_languages':
            return self.ascle.get_supported_translation_languages()
        elif action == 'tokens':
            return self.ascle.get_tokens()
        elif action == 'lemmas':
            return self.ascle.get_lemmas()
        elif action == 'dependency':
            return self.ascle.get_dependency()
        elif action == 'clusters':
            return self.ascle.get_clusters()
        elif action == 'multi_record_summary':
            return self.ascle.get_multi_record_summary()
        elif action == 'translation_mt5':
            return self.ascle.get_translation_mt5()
        elif action == 'med_question':
            return self.ascle.get_med_question()
        elif action == 'span_answer':
            return self.ascle.get_span_answer(command)
        elif action == 'choice':
            return self.ascle.get_choice(command)
        elif action == 'layman_text':
            return self.ascle.get_layman_text()
        elif action == 'interactive_chat':
            return self.ascle.get_dialogpt()
        else:
            return "Unknown action"

    def detect_language(self, command):
        """
        Detects the target language in the command for translation tasks.
        """
        if 'french' in command.lower():
            return 'French'
        elif 'spanish' in command.lower():
            return 'Spanish'
        elif 'german' in command.lower():
            return 'German'
        elif 'italian' in command.lower():
            return 'Italian'
        elif 'chinese' in command.lower():
            return 'Chinese'
        return 'French'  # Default to French

    def is_language_supported(self, language):
        """
        Checks if the language is supported by the translation system.
        """
        supported_languages = self.ascle.get_supported_translation_languages()
        return language in supported_languages

    def extract_text_for_similarity(self, command):
        """
        Extracts query_note and candidate_notes from the command for similarity comparison.
        """
        try:
            query_note = re.search(r"query_note='(.*?)'", command).group(1)
            candidate_notes = re.search(r"candidates='(.*?)'", command).group(1)
            return query_note, candidate_notes
        except AttributeError:
            return None, None

    def identify_action_with_zero_shot(self, command):
        """
        Uses zero-shot classification to identify the action from the command.
        """
        possible_actions = [
            'summarize', 'translate', 'named_entities', 'pos_tagging', 'abbreviations', 'hyponyms',
            'question_generation', 'similar_documents', 'linked_entities', 'supported_translation_languages',
            'tokens', 'lemmas', 'dependency', 'clusters', 'multi_record_summary', 'translation_mt5',
            'med_question', 'span_answer', 'choice', 'layman_text', 'interactive_chat'
        ]
        result = self.classifier(command, possible_actions, clean_up_tokenization_spaces=True, device=self.device)
        return result['labels'][0]
