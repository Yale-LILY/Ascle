# medical_processor.py

from Ascle import Ascle
from colorama import Fore

class MedicalProcessor:
    """
    MedicalProcessor handles medical text processing tasks using the Ascle package.
    It provides methods for summarization, translation, named entity recognition, and more.
    """

    def __init__(self):
        """
        Initializes the MedicalProcessor with an instance of the Ascle class.
        """
        self.med = Ascle()

    def summarize_text(self, text):
        """
        Summarizes the provided medical text.
        
        Parameters:
        text (str): The text to summarize.
        """
        print(f"{Fore.CYAN}System: Summarizing medical text...")
        self.med.update_and_delete_main_record(text)
        summary = self.med.get_layman_text(min_length=20, max_length=70)
        print(f"{Fore.CYAN}Summary:\n{summary}")
        return summary

    def translate_text(self, text, target_language):
        """
        Translates the provided medical text into the target language.
        
        Parameters:
        text (str): The text to translate.
        target_language (str): The target language for translation.
        """
        print(f"{Fore.CYAN}System: Translating medical text...")
        self.med.update_and_delete_main_record(text)
        translation = self.med.get_translation_mt5(target_language,clean_up_tokenization_spaces=True)
        print(f"{Fore.CYAN}Translation:\n{translation}")
        return translation
    def extract_named_entities(self, text):
        """
        Extracts named entities from the provided medical text.
        
        Parameters:
        text (str): The text from which to extract named entities.
        """
        print(f"{Fore.CYAN}System: Extracting named entities...")
        self.med.update_and_delete_main_record(text)
        entities = self.med.get_named_entities()
        print(f"{Fore.CYAN}Named Entities:\n{entities}")
        return entities

    def extract_linked_entities(self, text):
        """
        Extracts linked entities from the provided medical text.
        
        Parameters:
        text (str): The text from which to extract linked entities.
        """
        print(f"{Fore.CYAN}System: Extracting linked entities...")
        self.med.update_and_delete_main_record(text)
        linked_entities = self.med.get_linked_entities()
        print(f"{Fore.CYAN}Linked Entities:\n{linked_entities}")
        return linked_entities

    def pos_tagging(self, text):
        """
        Performs POS tagging on the provided medical text.
        
        Parameters:
        text (str): The text on which to perform POS tagging.
        """
        print(f"{Fore.CYAN}System: Performing POS tagging...")
        self.med.update_and_delete_main_record(text)
        pos_tags = self.med.get_pos_tagging(model_name="en_core_sci_sm")
        print(f"{Fore.CYAN}POS Tags:\n{pos_tags}")
        return pos_tags
    def extract_abbreviations(self, text):
        """
        Extracts abbreviations from the provided medical text.
        
        Parameters:
        text (str): The text from which to extract abbreviations.
        """
        print(f"{Fore.CYAN}System: Extracting abbreviations...")
        self.med.update_and_delete_main_record(text)
        abbreviations = self.med.get_abbreviations()
        print(f"{Fore.CYAN}Abbreviations:\n{abbreviations}")
        return abbreviations
    def extract_hyponyms(self, text):
        """
        Extracts hyponyms from the provided medical text.
        
        Parameters:
        text (str): The text from which to extract hyponyms.
        """
        print(f"{Fore.CYAN}System: Extracting hyponyms...")
        self.med.update_and_delete_main_record(text)
        hyponyms = self.med.get_hyponyms()
        print(f"{Fore.CYAN}Hyponyms:\n{hyponyms}")
        return hyponyms
    def generate_questions(self, text):
        """
        Generates questions from the provided medical text.
        
        Parameters:
        text (str): The text from which to generate questions.
        """
        print(f"{Fore.CYAN}System: Generating questions...")
        self.med.update_and_delete_main_record(text)
        questions = self.med.get_question()
        print(f"{Fore.CYAN}Generated Questions:\n{questions}")
        return questions
    def find_similar_documents(self, query_note, candidate_notes, top_k=3):
        """
        Finds similar documents to the query_note from the list of candidate_notes.
        
        Parameters:
        query_note (str): The main text to compare against candidate texts.
        candidate_notes (str): The candidate texts as a string separated by '|'.
        top_k (int): The number of top similar documents to return.
        """
        if query_note is None or candidate_notes is None:
            print(f"{Fore.RED}System: Missing input data for finding similar documents.")
            return
        
        # Split candidate_notes into a list
        candidate_notes_list = candidate_notes.split('|')
        self.med.update_and_delete_main_record(query_note)
        self.med.replace_supporting_records(candidate_notes_list)
        # Call the get_similar_documents function
        similar_docs = self.med.get_similar_documents(top_k)

        # Display the result
        if similar_docs.empty:
            print(f"{Fore.RED}System: No similar documents found.")
        else:
            print(f"{Fore.CYAN}Similar Documents:\n")
            print(similar_docs)
        return similar_docs
