
# 📔 UMLS Interface

<p align="center">
   <img src="Ascle_logo.png">
</p>

## Key Modules and Functions

### ✨ UmlsQA Class

The `UmlsQA` class allows interaction with a medical assistant model to process medical questions and return responses based on Unified Medical Language System (UMLS) terminology.

`__init__(self, model_name="gpt-4", api_key="")`: Initializes the medical assistant interface with the specified model and API key.

**Parameters**:
* `model_name`: The name of the language model to be used. Defaults to `"gpt-4"`.
* `api_key`: The API key for accessing the language model's API.

---

`ask_medical_question(self, question: str) -> str`: Ask a medical question and return the response from the medical assistant.

**Parameters**:
* `question`: A medical question to be processed.

**Returns**: 
* A `str` containing the generated response based on UMLS terminology.

**Example**:
```python
from umls_qa import UmlsQA

# Initialize the UmlsQA model
assistant = UmlsQA(model_name="gpt-3.5-turbo", api_key="xxxx")

# Define the medical question
question = "How does smoking affect lung function?"

# Print the response
print(assistant.ask_medical_question(question))
```
---

### ✨ ExtendedConversationBufferWindowMemory Class

The `ExtendedConversationBufferWindowMemory` class extends the memory handling of conversations by adding support for extra variables.

`load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]`: Load memory variables for a conversation, including extra variables.

**Parameters**:
* `inputs`: A dictionary containing the input variables for the memory.

**Returns**: 
* A `Dict[str, Any]` containing the loaded memory variables.

---
