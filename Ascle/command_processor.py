# command_processor.py

import re
from colorama import Fore
from transformers import pipeline
from medical_processor import MedicalProcessor
from api_manager import APIManager
import torch
class CommandProcessor:
    """
    CommandProcessor is responsible for handling user commands, identifying actions, 
    and delegating tasks to the appropriate processing functions.
    """

    def __init__(self, model_manager):
        """
        Initializes the CommandProcessor with a ModelManager instance.
        
        Parameters:
        model_manager (ModelManager): An instance of the ModelManager class.
        """
        self.history = []  # Initialize the history list to store conversation history
        self.device = 0 if torch.cuda.is_available() else -1

        self.model_manager = model_manager
        self.classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=self.device,clean_up_tokenization_spaces=True)
        self.medical_processor = MedicalProcessor()  # Initialize MedicalProcessor
        self.api_manager = APIManager(model_manager,self.history)  # Initialize APIManager
        self.action_synonyms = {
            'summarize': ['summarize', 'simplify', 'resume', 'abbreviate', 'condense', 'summarise'],
            'translate': ['translate', 'convert', 'change'],
            'named_entities': ['extract', 'find', 'identify', 'locate', 'detect entities'],
            'pos_tagging': ['tag', 'annotate', 'label', 'perform pos tagging'],
            'abbreviations': ['abbreviations', 'extract abbreviations', 'shorten', 'abbrev'],
            'hyponyms': ['hyponyms', 'specific terms', 'subordinate'],
            'question_generation': ['generate questions', 'question generation', 'questions'],
            'similar_documents': ['find similar documents', 'similar documents', 'related documents'],
            'linked_entities': ['linked entities', 'link entities', 'find linked entities', 'identify linked entities']
        }

    def process_command(self, command):
        """
        Processes a given command by identifying the action and topic, 
        and delegates the command to the appropriate model or function for execution.
        
        Parameters:
        command (str): The command input by the user.
        """
        print(f"\n{Fore.YELLOW}{'-' * 50}")
        print(f"{Fore.GREEN}User: {command}")
        print(f"\n{Fore.YELLOW}{'-' * 50}")
        
        if command.lower() == 'help':
            self.display_help()
            return
        elif command.lower() == 'show history':
            self.show_history()
            return

        # Normalize and parse commands for switching models
        if command.lower().startswith(('switch model to', 'change to', 'switch to')):
            # Extract the model name or number
            model_identifier = command.lower().replace('switch model to', '').replace('change to', '').replace('switch to', '').strip()
            if model_identifier in ['1', 'chatgpt']:
                self.model_manager.choose_model('1')
            elif model_identifier in ['2', 'claude']:
                self.model_manager.choose_model('2')
            elif model_identifier in ['3', 'gemini']:
                self.model_manager.choose_model('3')
            else:
                print(f"{Fore.RED}Invalid choice. Please select 'chatgpt', 'claude', or 'gemini' (or use numbers 1, 2, or 3).")
            return

        # Analyze the command and detect the action
        # Add user command to history
        self.history.append({"role": "user", "message": command})
        action = self.identify_action(command)
        detected_topic = self.detect_topic(command)
        #print(f"Action identified: {action}, Detected topic: {detected_topic}")

        # Delegate the command to appropriate handlers
        response =self.delegate_command(action, detected_topic, command)
        # Add system response to history
        self.history.append({"role": "system", "message": response})
        
    def identify_action(self, command):
        """
        Identifies the action requested in the command using predefined phrases 
        and zero-shot classification as a fallback.
        
        Parameters:
        command (str): The input command from the user.
        
        Returns:
        str: The identified action.
        """
        # Iterate over the command mappings to find a match in the input command
        for action, phrases in self.action_synonyms.items():
            for phrase in phrases:
                if re.search(rf"\b{phrase}\b", command, re.IGNORECASE):
                    return action  # Return the action as soon as a match is found

        # If no exact match is found, use zero-shot classification as a fallback
        return self.identify_action_with_zero_shot(command)

    def identify_action_with_zero_shot(self, command):
        """
        Uses zero-shot classification to identify the action in the command.
        
        Parameters:
        command (str): The input command from the user.
        
        Returns:
        str: The identified action.
        """
        possible_actions = list(self.action_synonyms.keys())
        result = self.classifier(command, possible_actions,clean_up_tokenization_spaces=True,device=self.device)
        action = result['labels'][0]  # The action with the highest score
        return action

    def detect_topic(self, command):
        """
        Detects the topic of the command using zero-shot classification.
        
        Parameters:
        command (str): The input command from the user.
        
        Returns:
        str: The detected topic.
        """
        # Define candidate labels (topics)
        labels = [
            "medical", "healthcare", "biology", "medicine", 
            "technology", "finance", "sports", "education", "entertainment"
        ]

        # Perform zero-shot classification
        result = self.classifier(command, candidate_labels=labels,clean_up_tokenization_spaces=True,device=self.device)

        # Get the label with the highest score
        detected_topic = result['labels'][0]

        # Check for medical keywords if the detected topic isn't already medical
        medical_keywords = [
            'cells', 'immunosuppressive', 'disease', 'virus', 'neurons', 'arthritis', 'treatment', 'symptoms'
            # Add more medical keywords here
        ]

        if detected_topic != 'medical':
            if any(keyword.lower() in command.lower() for keyword in medical_keywords):
                detected_topic = 'medical'

        return detected_topic

    

    def delegate_command(self, action, topic, command):
        """
        Delegates the command to the appropriate handler based on the identified action and topic.
        
        Parameters:
        action (str): The identified action to be performed.
        topic (str): The detected topic of the command.
        command (str): The full command issued by the user.
        
        Returns:
        str: The response generated by the system.
        """
        response = None  # Initialize response

        if topic == 'medical' or topic == 'medicine' or topic == 'healthcare':
            # Call the corresponding method in MedicalProcessor
            if action == 'summarize':
                text = self.extract_text_from_command(command)
                response = self.medical_processor.summarize_text(text)
            elif action == 'translate':
                text = self.extract_text_from_command(command)
                target_language = self.detect_language(command)
                response = self.medical_processor.translate_text(text, target_language)
            elif action == 'named_entities':
                text = self.extract_text_from_command(command)
                response = self.medical_processor.extract_named_entities(text)
            elif action == 'linked_entities':
                text = self.extract_text_from_command(command)
                response = self.medical_processor.extract_linked_entities(text)
            elif action == 'pos_tagging':
                text = self.extract_text_from_command(command)
                response = self.medical_processor.pos_tagging(text)
            elif action == 'abbreviations':
                text = self.extract_text_from_command(command)
                response = self.medical_processor.extract_abbreviations(text)
            elif action == 'hyponyms':
                text = self.extract_text_from_command(command)
                response = self.medical_processor.extract_hyponyms(text)
            elif action == 'question_generation':
                text = self.extract_text_from_command(command)
                response = self.medical_processor.generate_questions(text)
            elif action == 'similar_documents':
                query_note, candidate_notes = self.extract_text_for_similarity(command)
                response = self.medical_processor.find_similar_documents(query_note, candidate_notes)
            else:
                response = "System: Sorry, I don't understand that medical command."
        else:
            # Use the selected model via APIManager
            if self.model_manager.get_selected_model() == 'ChatGPT':
                response = self.api_manager.call_chatgpt_api(command)
            elif self.model_manager.get_selected_model() == 'Claude':
                response = self.api_manager.call_claude_api(command)
            elif self.model_manager.get_selected_model() == 'Gemini':
                response = self.api_manager.call_gemini_api(command)
            else:
                response = "System: Sorry, I don't understand that command for the general topic."
        
        # Return the response to be stored in the history
        return response
    
    def extract_text_from_command(self, command):
        """
        Extracts text from the command after identifying the action part.
        
        Parameters:
        command (str): The full command issued by the user.
        
        Returns:
        str: The extracted text to be processed.
        """
        # Extract the action prefix from the command and strip it to get the main text
        for action, phrases in self.action_synonyms.items():
            for phrase in phrases:
                match = re.search(fr"(?i){phrase}.*:", command)
                if match:
                    # Extract text that comes after the action phrase
                    return command[len(match.group(0)):].strip()
        return command

    def detect_language(self, command):
        """
        Detects target language in translation requests.
        
        Parameters:
        command (str): The input command from the user.
        
        Returns:
        str: The detected target language (default to 'French').
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
        # Add more languages as needed
        return 'French'  # Default to French if no language is specified

    def extract_text_for_similarity(self, command):
        """
        Extracts the query_note and candidate_notes from the command.
        
        Example command format:
        "find similar documents: query_note='text here' candidates='text1 | text2 | text3'"
        
        Returns:
        - query_note: The main text.
        - candidate_notes: The candidate texts as a string separated by '|'.
        """
        try:
            # Extract query_note and candidate_notes from the command
            query_note = re.search(r"query_note='(.*?)'", command).group(1)
            candidate_notes = re.search(r"candidates='(.*?)'", command).group(1)
            return query_note, candidate_notes
        except AttributeError:
            # Return None if extraction fails
            return None, None
        
    def show_history(self):
        """
        Displays the conversation history.
        """
        print(f"\n{Fore.CYAN}{'-' * 50}")
        print("Conversation History:")
        for entry in self.history:
            role = entry['role'].capitalize()
            message = entry['message']
            print(f"{role}: {message}")
        print(f"{Fore.CYAN}{'-' * 50}\n")
        
    def display_help(self):
        """
        Displays help information for the available commands.
        """
        print(f"{Fore.CYAN}Available Commands and Examples:\n")
        # Add detailed help information here for each action
        
        # Summarize
        print("1. Summarize:")
        print("   Command: summarize: 'Enter the text you want to summarize here.'")
        print("   Example: summarize: 'Artificial intelligence (AI) is intelligence demonstrated by machines.'")
        print()

        # Translate
        print("2. Translate:")
        print("   Command: translate to [language]: 'Enter the text you want to translate here.'")
        print("   Example: translate to French: 'Artificial intelligence is transforming industries.'")
        print()

        # Abbreviations
        print("3. Abbreviations:")
        print("   Command: find abbreviations in: 'Enter the text here.'")
        print("   Example: find abbreviations in: 'The patient has a history of COPD and CHF.'")
        print()

        # Linked Entities
        print("4. Linked Entities:")
        print("   Command: find linked entities in: 'Enter the text here.'")
        print("   Example: find linked entities in: 'Aspirin is used to reduce fever and relieve mild to moderate pain.'")
        print()

        # Named Entities
        print("5. Named Entities:")
        print("   Command: find named entities in: 'Enter the text here.'")
        print("   Example: find named entities in: 'Albert Einstein was a theoretical physicist who developed the theory of relativity.'")
        print()

        # POS Tagging
        print("6. POS Tagging:")
        print("   Command: perform pos tagging on: 'Enter the text here.'")
        print("   Example: perform pos tagging on: 'AI is the simulation of human intelligence processes by machines.'")
        print()

        # Hyponyms
        print("7. Hyponyms:")
        print("   Command: find hyponyms in: 'Enter the text here.'")
        print("   Example: find hyponyms in: 'Vehicle such as car, truck, and bicycle.'")
        print()

        # Question Generation
        print("8. Question Generation:")
        print("   Command: generate questions for: 'Enter the text here.'")
        print("   Example: generate questions for: 'Machine learning is a type of AI that allows software applications to become more accurate in predicting outcomes.'")
        print()

        # Similar Documents
        print("9. Similar Documents:")
        print("   Command: find similar documents: query_note='Enter the main text here' candidates='Enter candidate texts separated by |'")
        print("   Example: find similar documents: query_note='Neurons are the fundamental units of the brain.' candidates='A neural network is a series of algorithms... | Aspirin is used to relieve pain... | People can buy aspirin over the counter...'\n")

        print(f"{Fore.CYAN}Type 'quit' to exit the program.\n")
