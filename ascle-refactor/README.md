
# Ascle Toolkit

## Overview

The Ascle Toolkit is a modular and extensible toolkit for medical text processing. It includes a suite of tools for natural language processing (NLP), such as entity extraction, summarization, and translation, tailored to medical use cases. The toolkit is designed to integrate different NLP frameworks and models, providing users with flexibility and powerful capabilities for processing medical texts.

## Key Features

- **Multi-tool Integration**: Supports various NLP tools, including Stanza, SciSpacy, and PyRuSH.
- **Medical Text Processing**: Uses Medspacy for entity extraction and identifying sections in medical text.
- **Extensible Framework**: Easily add new processors and NLP models to expand functionality.
- **Utilities for Summarization and Translation**: Leverages transformers for summarizing and translating medical documents.

## Project Structure

```
ascle/
├── core/
│   ├── base.py            # Base classes for processors
│   ├── ascle.py           # Main Ascle class
├── models/
│   ├── manager.py         # Model management
├── processors/
│   ├── text/
│   │   ├── nlp_processor.py           # NLPProcessor for various NLP tools
│   │   ├── summarization_processor.py # Summarization using transformers
│   │   ├── translation_processor.py   # Translation using MT5
│   ├── medical/
│   │   ├── medspacy_processor.py      # Medical text processing using Medspacy
├── utils/
│   ├── config.py          # Configuration management
├── tests/
│   ├── unit/              # Unit tests for components
│   ├── integration/       # Integration tests
├── docs/
│   ├── api/               # API documentation
│   ├── examples/          # Example use cases
```

## Installation

Clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd ascle
pip install -r requirements.txt
```

Alternatively, you can use Poetry for dependency management:

```bash
poetry install
```

## Quick Start

Here's a quick example to get started with the Ascle Toolkit:

```python
from ascle.core.ascle import Ascle

# Initialize Ascle and process text using default processors
with Ascle() as ascle:
    text = "The patient presents with fever and cough."
    results = ascle.process_text(text)
    print(results)
```

## Usage Examples

### Summarization

Use the summarization processor to summarize medical notes:

```python
from ascle.core.ascle import Ascle

with Ascle() as ascle:
    text = "The patient presents with acute respiratory symptoms. The doctor suggested staying at home."
    result = ascle.process_text(text, processors=["summarization"])
    print(result["summarization"])
```

### Translation

Translate medical text into other languages using MT5:

```python
from ascle.core.ascle import Ascle

with Ascle() as ascle:
    text = "The patient presents with acute respiratory symptoms."
    result = ascle.process_text(text, processors=["translation"])
    print(result["translation"])
```

## Configuration

You can configure the toolkit by using the `AscleConfig` class to specify model parameters and processing options:

```python
from ascle.utils.config import AscleConfig

config = AscleConfig(model={"name": "microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract", "device": "cuda"})
ascle = Ascle(config)
```

## Testing

To run the unit tests and verify the functionality of the toolkit, use `pytest`:

```bash
pytest tests/unit/
```

## Documentation

Comprehensive API documentation can be found in the `docs/api/` folder. Example use cases and tutorials are available in the `docs/examples/` folder.

## Contributing

Contributions are welcome! Please fork the repository, make changes, and submit a pull request. Ensure that all changes are covered by unit tests.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.
