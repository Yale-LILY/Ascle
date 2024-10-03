
# **User Guide for Model Integration and Command Processing**

This guide provides a detailed description of how to use the available classes and methods to manage and process requests through various language models. The structure is organized around the main classes and functions, allowing users to select models, configure corresponding APIs, and process prompts efficiently.

## **1. Class `ModelManager`**

### **Overview**
The `ModelManager` class is responsible for model management and API key handling. It facilitates model selection, default version management, and retrieving API keys for external model calls.

### **Parameters**
- `config_file` (str, optional): Path to the environment configuration file. Defaults to `.env`.

### **Main Methods**

#### **`__init__(self, config_file=".env")`**
- **Description**: Initializes the class by loading API keys from the configuration file.
- **Return**: None.

#### **`choose_model(self, model, model_version=None)`**
- **Description**: Selects the model and its version. If no version is specified, the default version is used.
- **Parameters**:
  - `model` (str): Name of the model (`chatgpt`, `claude`, `gemini`, `llama`, `ascle`).
  - `model_version` (str, optional): Version of the model. Defaults to the predefined version.
- **Return**: Boolean indicating if the selection was successful.

#### **`get_selected_model(self)`**
- **Description**: Returns the currently selected model.
- **Return**: Name of the selected model (str).

#### **`get_default_version(self, model)`**
- **Description**: Retrieves the default version of a specific model.
- **Parameters**:
  - `model` (str): Model name.
- **Return**: Default version of the model (str).

#### **`get_api_key(self, model_name)`**
- **Description**: Retrieves the API key for the specified model.
- **Parameters**:
  - `model_name` (str): Name of the model.
- **Return**: API key (str) or `None` if no key exists.

---

## **2. Class `APIManager`**

### **Overview**
The `APIManager` class handles API calls for specific models such as `ChatGPT`, `Claude`, `Gemini`, and `Llama`. It implements a common call flow and can easily adapt to new APIs.

### **Parameters**
- `model_manager` (`ModelManager`): Instance of `ModelManager` to retrieve API keys and manage model versions.

### **Main Methods**

#### **`configure_api(self, model_name)`**
- **Description**: Configures the credentials and tokens necessary to access the model APIs.
- **Parameters**:
  - `model_name` (str): Name of the model to configure (e.g., `gemini`, `llama`).
- **Return**: None.

#### **`call_model_api(self, model_name, text, model)`**
- **Description**: Makes an API call to the selected model.
- **Parameters**:
  - `model_name` (str): Name of the model (e.g., `chatgpt`, `claude`).
  - `text` (str): Input text to be processed by the model.
  - `model` (str): Version of the model.
- **Return**: Model's generated response (str).

---

## **3. Class `AscleInterface`**

### **Overview**
The `AscleInterface` class facilitates interaction between available models and the user. This class allows selecting a model (including `Ascle`) and managing command execution using a unified workflow.

### **Parameters**
None.

### **Main Methods**

#### **`choose_model(self, model, **model_versions)`**
- **Description**: Selects the primary model and its version (if applicable). If the model is `Ascle`, it is set up to handle internal tasks.
- **Parameters**:
  - `model` (str): Name of the model (`gpt`, `gemini`, `claude`, `llama`, `ascle`).
  - `model_versions` (dict, optional): Dictionary that allows specifying custom versions for models.
- **Return**: None.

#### **`process_prompt(self, prompt)`**
- **Description**: Processes an input text (`prompt`) based on the selected model. If using the `Ascle` model, it handles internal tasks; otherwise, it delegates the call to `APIManager`.
- **Parameters**:
  - `prompt` (str): Input text to be processed.
- **Return**: Generated response (str).

---

## **4. Class `CommandProcessor`**

### **Overview**
The `CommandProcessor` class is responsible for identifying and processing commands using the `Ascle` model. It also manages command classification and the use of other models when needed.

### **Parameters**
- `model_manager` (`ModelManager`): Instance of `ModelManager` to manage models.

### **Main Methods**

#### **`identify_action_with_zero_shot(self, command)`**
- **Description**: Uses zero-shot classification to identify the action to be performed with the input command.
- **Parameters**:
  - `command` (str): Input command to be processed.
- **Return**: Identified action (str).

#### **`process_ascle_prompt(self, prompt, ascle, model_ascle=None)`**
- **Description**: Processes a command using the `Ascle` model based on the identified action. Adapts the workflow for tasks such as summarization, question generation, etc.
- **Parameters**:
  - `prompt` (str): Input command or text.
  - `ascle` (`Ascle`): Instance of `Ascle` to process the command.
  - `model_ascle` (str, optional): Version of the `Ascle` model.
- **Return**: Processed response based on the action (str).

---

## **5. Example Usage: `AscleInterface`**

### **Overview**
The following is an example of how to use the `AscleInterface` class to select the `Ascle` model and process an input text to generate a summary.

### **Example Code**

```python
from Ascle_interface import AscleInterface

# Create an instance of AscleInterface
med = AscleInterface()

# Define the input text (prompt)
prompt = ("summarize this text: The patient presents with symptoms of acute bronchitis, "
          "including cough, chest congestion, and mild fever. Auscultation reveals coarse breath sounds "
          "and occasional wheezing...")

# Select the Ascle model
med.choose_model("ascle")

# Process the prompt and get the output
output = med.process_prompt(prompt)
print("Output:", output)
```

---

This guide provides a clear structure for users to understand how to use the classes, select models, and process commands using the available tools.
