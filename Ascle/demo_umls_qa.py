# Import the necessary classes
from umls_qa import UmlsQA

# Code that will be called from the main
if __name__ == "__main__":
    
    # Initialize the UmlsQA 
    assistant = UmlsQA(model_name="gpt-3.5-turbo", api_key="xxxx")  
    
    # Define the medical question in a variable
    question = "How does smoking affect lung function?"
    
    # Ask the medical question and get the response
    response = assistant.ask_medical_question(question)  
    
    # Print the response in English
    print(f"Response: {response}")
