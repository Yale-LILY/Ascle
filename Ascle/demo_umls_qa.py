# Import the necessary classes
from model_manager import ModelManager  # Import ModelManager to manage API keys
from medical_assistant import MedicalAssistantInterface  # Import MedicalAssistantInterface class

# Code that will be called from the main
if __name__ == "__main__":
    # Initialize the ModelManager, which loads the API keys from the .env file
    model_manager = ModelManager(config_file=".env")  
    
    # Initialize the UmlsQA using the model manager to handle API keys
    assistant = UmlsQA(model_manager=model_manager)  
    
    # Define the medical question in a variable
    question = "How does smoking affect lung function?"
    
    # Ask the medical question and get the response from the assistant
    response = assistant.ask_medical_question(question)  
    
    # Print the response in English
    print(f"Response: {response}")
