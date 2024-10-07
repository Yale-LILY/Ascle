
# 📔 Use of Ascle and Model Integration

<p align="center">
   <img src="Ascle_logo.png">
</p>

## Key Modules and Functions

### ✨ Claude Integration

`call_Claude(model_name="claude-1.3", api_key="")`: Interacts with the Anthropic Claude model to generate a completion response.

**Parameters**:
* `model_name`: The name of the Claude model to be used. Defaults to `"claude-1.3"`.
* `api_key`: The API key for accessing Claude's API.
* returns: A string with the generated response from Claude.

**Example**:
```python
from Ascle import Ascle

med = Ascle()
prompt = ("Summarize this text: The patient presents with symptoms of acute bronchitis...")

med.update_and_delete_main_record(prompt)

# Using the default model
response_default = med.call_Claude(api_key="xxxx")

# Using a specific Claude model
response_specific = med.call_Claude(model_name="claude-2", api_key="xxxx")
```
---

### ✨ GPT Integration

`call_GPT(model_name="gpt-4", api_key="")`: Sends a query to OpenAI's GPT-4 model and retrieves a generated response.

**Parameters**:
* `model_name`: The name of the GPT model to be used. Defaults to `"gpt-4"`.
* `api_key`: The API key for accessing OpenAI's GPT API.
* returns: A string with the generated response from GPT.

**Example**:
```python
from Ascle import Ascle

med = Ascle()
prompt = "Summarize the following text: ..."
med.update_and_delete_main_record(prompt)

# Using the default model
response_default = med.call_GPT(api_key="xxxx")

# Using a specific GPT model
response_specific = med.call_GPT(model_name="gpt-3.5-turbo", api_key="xxxx")
```
---

### ✨ Gemini Integration

`call_Gemini(model_name="gemini-1.5-flash", api_key="")`: Interacts with the Gemini model, using the provided API key to generate content.

**Parameters**:
* `model_name`: The name of the Gemini model to be used. Defaults to `"gemini-1.5-flash"`.
* `api_key`: The API key for accessing Gemini's API.
* returns: A string with the generated response from Gemini.

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

### ✨ LLaMA Integration

`call_LlaMa(model_name="meta-llama/Llama-2-7b-chat-hf", api_key="")`: Utilizes the Meta LLaMA model to generate text responses based on user input.

**Parameters**:
* `model_name`: The name of the LLaMA model to be used. Defaults to `"meta-llama/Llama-2-7b-chat-hf"`.
* `api_key`: The API key for accessing Meta's LLaMA model.
* returns: A string with the generated response from LLaMA.

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
