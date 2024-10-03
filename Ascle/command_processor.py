import re
from transformers import pipeline
from api_manager import APIManager
from Ascle import Ascle
import transformers
import torch
import re
import ast
class CommandProcessor:
    def __init__(self, model_manager):
        """
        Initializes the CommandProcessor with a ModelManager instance and sets up zero-shot classification.
        """
        transformers.logging.set_verbosity_error()
        self.device = 0 if torch.cuda.is_available() else -1
        self.model_manager = model_manager
        self.classifier = pipeline(
            "zero-shot-classification", 
            model="facebook/bart-large-mnli", 
            device=self.device, 
            clean_up_tokenization_spaces=True
        )
        self.api_manager = APIManager(model_manager)
        self.ascle = Ascle()

    def process_ascle_prompt(self, prompt, ascle, model_ascle=None):
        """
        Process a prompt using Ascle models based on the identified action. 
        This method was previously part of AscleInterface and is now integrated here.
        """
        action = self.identify_action_with_zero_shot(prompt)
        prompt = prompt.split(":", 1)[1].strip()
        
        #prompt = prompt.split(":")[1].strip()
        ascle.update_and_delete_main_record(prompt)
        if model_ascle:
            # Update Ascle models if a specific model is provided
            if action in ['multi_choice_qa']:
                ascle.update_bert_model(model_ascle)  # Example: PubMedBERT fine-tuned for HEADQA
            elif action in ['simplify_text']:
                ascle.update_scispacy_model(model_ascle)  # Example: BART fine-tuned for eLife
            elif action in ['translate']:
                ascle.update_marian_model(model_ascle)  # Example: mT5 fine-tuned for en_es translation

        # Process the identified action
        if action == 'summarize' or action == 'simplify_text':  
            return ascle.get_single_record_summary()
        elif action == 'translate':
            target_language = self.detect_language(prompt)
            if self.is_language_supported(target_language):
                return ascle.get_translation(target_language)
            return f"Error: The language '{target_language}' is not supported for translation."
        elif action == 'layman_translation':
            return ascle.get_layman_text(model_name=model_ascle) if model_ascle else ascle.get_layman_text()

        elif action == 'named_entities':
            return ascle.get_named_entities()
        elif action == 'linked_entities':
            return ascle.get_linked_entities()
        elif action == 'pos_tagging':
            return ascle.get_pos_tags()
        elif action == 'abbreviations':
            return ascle.get_abbreviations()
        elif action == 'hyponyms':
            return ascle.get_hyponyms()
        elif action == 'clusters':
            record, candidates = self.extract_text_for_similarity(prompt)
            ascle.update_and_delete_main_record(record)
            ascle.replace_supporting_records(candidates)
            return ascle.get_clusters()
        elif action == 'sentencizer':
            return ascle.get_sentences(model_ascle)[0] if model_ascle else ascle.get_sentences()[0]
        elif action == 'question_generation':
            return ascle.get_question(model_name=model_ascle) if model_ascle else ascle.get_question()
        elif action == 'multi_choice_qa': 
            text, question, choices, num_labels = self.extract_question_and_choices_from_prompt(prompt)
            ascle.update_and_delete_main_record(question)
            return ascle.get_choice(text, question, choices, num_labels)
        elif action == 'span_answer': 
            question, content = self.extract_question_and_content_from_prompt(prompt)
            ascle.update_and_delete_main_record(question)
            return ascle.get_span_answer(content)
        elif action == 'similar_documents':            
            record, candidates = self.extract_text_for_similarity(prompt)
            ascle.update_and_delete_main_record(record)
            ascle.replace_supporting_records(candidates)
            return ascle.get_similar_documents()
        
        else:
            return "Ascle model action not recognized."

    def detect_language(self, command):
        """
        Detects the target language in the command for translation tasks.
        """
        languages = {'french': 'French', 'spanish': 'Spanish', 'german': 'German', 'italian': 'Italian', 'chinese': 'Chinese'}
        for lang, name in languages.items():
            if lang in command.lower():
                return name
        return 'French'  # Default to French

    def is_language_supported(self, language):
        """
        Checks if the language is supported by the translation system.
        """
        supported_languages = self.ascle.get_supported_translation_languages()
        return language in supported_languages

    def extract_text_for_similarity(self,prompt):
        """
        Extracts the 'record' and 'candX' variables from the given prompt.
        The prompt contains a 'record' and multiple candidates ('cand1', 'cand2', etc.).
        """
        # Use regex to extract the content of the "record" and the "candX" candidates
        record_match = re.search(r'record\s*=\s*"(.*?)"', prompt, re.DOTALL)
        candidates_matches = re.findall(r'cand\d+\s*=\s*"(.*?)"', prompt, re.DOTALL)

        # Ensure we found the record
        if not record_match:
            raise ValueError("No 'record' found in the prompt.")

        # The record is the main text we want to compare
        record = record_match.group(1).replace("\\", "").strip()

        # The candidates are the texts we want to compare against the record
        candidates = [candidate.replace("\\", "").strip() for candidate in candidates_matches]

        return record, candidates

    
    def extract_question_and_choices_from_prompt(self,prompt):
        """
        Extract the question and choices from the prompt with variable assignments.
        Example format:
            text = ""
            question = "The excitatory postsynaptic potentials:"
            choices = ["They are all or nothing.", "They are hyperpolarizing.", ...]
        """
        print(prompt)
        text_match = re.search(r'text\s*=\s*"(.*?)"', prompt)
        # Extract the question using regex
        question_match = re.search(r'question\s*=\s*"(.*?)"', prompt)
        
        # Extract the choices as a Python list using regex
        choices_match = re.search(r'choices\s*=\s*(\[.*?\])', prompt, re.DOTALL)

        # Ensure we found the text
        if not text_match:
            raise ValueError("No 'text' found in the prompt.")
        # Ensure we found the question
        if not question_match:
            raise ValueError("No 'question' found in the prompt.")
        
        # Ensure we found the choices
        if not choices_match:
            raise ValueError("No 'choices' found in the prompt.")

        # Extract and clean up the text
        text = text_match.group(1).strip()
        # The question is the main text we want to answer
        question = question_match.group(1).strip()

        # Use `ast.literal_eval` to safely evaluate the list structure in the prompt
        choices = ast.literal_eval(choices_match.group(1).strip())
        num_choices = len(choices)
        return text, question, choices, num_choices
    def extract_question_and_content_from_prompt(self, prompt):
        """
        Extract the question and content from a given prompt.
        The prompt contains 'question = ...' and 'content = ...'.
        """
        # Extract the question using regex
        question_match = re.search(r'question\s*=\s*"(.*?)"', prompt)
        
        # Extract the content using regex
        content_match = re.search(r'content\s*=\s*"(.*?)"', prompt)

        # Ensure we found the question
        if not question_match:
            raise ValueError("No 'question' found in the prompt.")
        
        # Ensure we found the content
        if not content_match:
            raise ValueError("No 'content' found in the prompt.")
        
        # Extract and clean up the question and content
        question = question_match.group(1).strip()
        content = content_match.group(1).strip()

        return question, content
    
    def identify_action_with_zero_shot(self, command):
        """
        Uses zero-shot classification to identify the action from the command.
        """
        possible_actions = [
            'summarize', 'translate', 'named_entities', 'pos_tagging', 'abbreviations', 
            'hyponyms', 'question_generation', 'similar_documents', 'linked_entities',
            'supported_translation_languages', 'tokens', 'lemmas', 'dependency', 
            'clusters', 'multi_record_summary', 'translation_mt5', 'med_question', 
            'span_answer', 'choice', 'layman_text', 'interactive_chat', 'sentencizer',
            'multi_choice_qa', 'layman_translation'
        ]
        result = self.classifier(command, possible_actions, clean_up_tokenization_spaces=True, device=self.device)
        #print(result['labels'])
        return result['labels'][0]
