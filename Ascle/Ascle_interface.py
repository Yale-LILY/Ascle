from model_manager import ModelManager
from api_manager import APIManager
from command_processor import CommandProcessor
from Ascle import Ascle
import warnings

class AscleInterface:
    def __init__(self):
        """
        Initializes AscleInterface with the ModelManager, APIManager, Ascle, 
        and CommandProcessor for analyzing user input and processing actions.
        """
        warnings.filterwarnings("ignore", message="Can't initialize NVML")
        self.model_manager = ModelManager()
        self.ascle = Ascle()
        self.command_processor = CommandProcessor(self.model_manager)
        self.api_manager = APIManager(self.model_manager)
        self.using_ascle_model = False
        self.model = None

    def choose_model(self, model, **model_versions):
        """
        Choose the primary model and update its version if provided. 
        Automatically defaults to a model's default version if not specified.

        Parameters:
        model (str): The primary model to use (e.g., 'gpt', 'gemini', 'claude', 'llama', 'ascle').
        """
        self.model = model
        if model == 'ascle':
            self.using_ascle_model = True
            version = model_versions.get(f"model_{model}") or self.model_manager.get_default_version(model)
            self.model_manager.choose_model(model, version)
        else:
            version = model_versions.get(f"model_{model}") or self.model_manager.get_default_version(model)
            self.model_manager.choose_model(model, version)
    def process_prompt(self, prompt):
        """
        Process the input prompt based on the selected model (Ascle or open models).
        Returns the result of processing the prompt.
        """
        if self.using_ascle_model:
            return self.command_processor.process_ascle_prompt(prompt, self.ascle,self.model_manager.get_selected_model())
        return self.api_manager.call_model_api(self.model, prompt, self.model_manager.get_selected_model())
