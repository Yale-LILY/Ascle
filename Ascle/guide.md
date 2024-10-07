
# **Use of Ascle and Model Integration**
## `call_Claude`

**Description**:  
This method interacts with the Anthropic Claude model to generate a completion response based on the user's input. It takes the current main record stored in the class, sends it to Claude, and retrieves the model's response.

**Parameters**:
- `model_name` (`str`, optional): The name of the Claude model to be used. Defaults to `"claude-1.3"`.
- `api_key` (`str`, optional): The API key to authenticate the request to the Anthropic Claude model.

**Returns**:
- `str`: The generated response from Claude, or an error message if no content is found.

**Example**:
```python
from Ascle import Ascle

med = Ascle()
prompt = ("summarize this text: The patient presents with symptoms of acute bronchitis, "
          "including cough, chest congestion, and mild fever. Auscultation reveals coarse breath sounds "
          "and occasional wheezing. Based on the clinical examination, a diagnosis of acute bronchitis is made, "
          "and the patient is prescribed a short course of bronchodilators and advised to rest and stay hydrated.")

med.update_and_delete_main_record(prompt)

# Using the default model
response_default = med.call_Claude(api_key="xxxx")

# Using a specific Claude model
response_specific = med.call_Claude(model_name="claude-2", api_key="xxxx")
```

---

## `call_GPT`

**Description**:  
This method sends the user's input to OpenAI's GPT-4 model using the provided API key and model name. It constructs a request, submits it to OpenAI's API, and returns the generated response from GPT-4.

**Parameters**:
- `model_name` (`str`, optional): The name of the GPT model to be used. Defaults to `"gpt-4"`.
- `api_key` (`str`, optional): The API key to authenticate the request to OpenAI's API.

**Returns**:
- `str`: The generated response from GPT-4, or an error message with the HTTP status code and response if the call fails.

**Example**:
```python
from Ascle import Ascle

med = Ascle()
prompt = "Summarize the following text: ..."
med.update_and_delete_main_record(prompt)

# Using the default model
response_default = med.call_GPT(api_key="xxxx")

# Using a specific GPT model
response_specific = med.call_GPT(model_name="gpt-3.5-turbo",api_key="xxxx")
```
---

## `call_Gemini`

**Description**:  
This method interacts with the Gemini model, using the provided API key to generate content based on the user's main record. It configures the API and generates content from the specified Gemini model.

**Parameters**:
- `model_name` (`str`, optional): The name of the Gemini model to be used. Defaults to `"gemini-1.5-flash"`.
- `api_key` (`str`, optional): The API key to authenticate the request to the Gemini model.

**Returns**:
- `str`: The generated response from Gemini based on the user's input.


**Example**:
```python
from Ascle import Ascle

med = Ascle()
prompt = "Summarize the following text: ..."
med.update_and_delete_main_record(prompt)

# Using the default model
response_default = med.call_Gemini(api_key="xxxx")

# Using a specific Gemini model
response_specific = med.call_Gemini(model_name="gemini-2.0", api_key="xxxx")
```

---

## `call_LlaMa`

**Description**:  
This method utilizes the Meta LLaMA model to generate text responses based on user input. The method handles model login, tokenization, and leverages a pre-trained LLaMA model for generating text.

**Parameters**:
- `model_name` (`str`, optional): The name of the LLaMA model to be used. Defaults to `"meta-llama/Llama-2-7b-chat-hf"`.
- `api_key` (`str`, optional): The API key used for authentication and access to the LLaMA model.

**Returns**:
- `str`: The generated response from the LLaMA model based on the input provided.

**Example**:
```python
from Ascle import Ascle

med = Ascle()
prompt = "Summarize the following text: ..."
med.update_and_delete_main_record(prompt)

# Using the default model
response_default = med.call_LlaMa(api_key="xxxx")

# Using a specific LLaMa model
response_specific = med.call_LlaMa(model_name="meta-llama/Llama-2-13b-chat-hf", api_key="xxxx")
```

```
