
 # 📔 Documentation

<img src="Ascle_logo.png" alt="drawing" width="1000"/> 

A comprehensive natural language processing (NLP) toolkit designed specifically for medical text processing.
## Key Modules and Functions

### ✨multi_doc_functions.py 

`get_similar_documents(bert_model, query_note, candidate_notes, candidates, top_k)`: find similar documents/records given the query record ID number, return the `top_k` results.

**Parameters**:
* `bert_model`: the name of the bert model
* `query_note`: query note, string
* `candidate_notes`: candiate note, a list of string
* `candidates`: a list of candidate ID, a list of int
* `top_k`: the number of return results, default value is 2
* returns a `DataFrame` with candidate_note_id, similarity_score, and candidate_text

`get_clusters(bert_model, notes, k=2)`: Use K-means to cluster the records using pretrained bert encoding into `k` clusters. 

**Parameters**:
* `bert_model`: the name of the bert model
* `top_k`: the number of clusters, default value is 2
* returns a `DataFrame` object...

### ✨scispacy_functions.py
`get_abbreviations(model, text)`: get abbreviations and their meanings of the input text.

**Parameters**:
* `model`: model name, supports Spacy models
* `text` : input text, string
* returns a list of tuples in the form (abbreviation, expanded form), each element being a str

`get_hyponyms(model, text)`: get hyponyms of the recognized entities in the input text.

**Parameters**:
* `model`: model name, supports Spacy models
* `text` : input text, string
* returns a list of tuples in the form (hearst_pattern, entity_1, entity_2, ...), each element being a str

`get_linked_entities(model, text)`: get linked entities in the input text.

**Parameters**:
* `model`: model name, supports Spacy models
* `text` : input text, string
* returns a dictionary in the form {named entity: list of strings each describing one piece of linked information}

`get_named_entities(model, text)`: get named entities in the input text.

**Parameters**:
* `model`: model name, supports Spacy models
* `text` : input text, string
* returns a list of strings, each string is an identified named entity

### ✨transformer_functions.py
`get_supported_translation_languages()`: returns a list of support target language names in string.

`get_translation(text, model_name, target_language)`: translate the input text into the target language.

**Parameters**:
* `text`: input text in string
* `model_name`: bert model name in string
* `target_language`: target language name from the supported language list
* returns a string, which is the translated version of the text]

`get_mT5_translation(text, target_language)`: translate the input text into the target language using fine-tuned multilingual T5 models.

**Parameters**:
* `text`: input text in string (English)
* `target_language`: target language name from the supported language list
* returns a string, which is the translated version of the text]

`get_bert_embeddings(pretrained_model, texts)`: encode the input text with pretrained bert model

**Parameters**:
* `pretrained_model`: bert model name in string
* `texts`: input text in a list of string  
* returns a list of lists of sentences, each list is made up of sentences from the same document


`get_single_summary(text,model_name,min_length,max_length)`: single document text summarization

**Parameters**:
* `text`: input string text
* `model_name`: model_name: `bart-large-cnn`', '`t5-small`', '`t5-base`', '`t5-large`', '`t5-3b`', '`t5-11b`
* `min_length`: min length in summary
* `max_length`: max length in summary
* returns the summary string

`get_multi_summary_joint(text, model_name, min_length, max_length)`: text summarization, given multiple documents (Join all the input documents as a long document, then do single document summarization) 

**Parameters**:
* `text`: input sequence: a list of string
* `model_name`: model_name: `bart-large-cnn`', '`t5-small`', '`t5-base`', '`t5-large`', '`t5-3b`', '`t5-11b`
* `min_length`: min length in summary
* `max_length`: max length in summary
* returns the summary string


`get_span_answer(question, context, model_name)`: question answering, given question and context, return the answer in a string format

**Parameters**:
* `question`: the question, input sequence as a string
* `context`: related context, input sequence as a string
* `model_name`: choices:`sultan/BioM-ELECTRA-Large-SQuAD2`, `deepset/roberta-base-squad2`, `AnonymousSub/SciFive_MedQuAD_question_generation`
* returns a string as the answer


`get_question(context, model_name)`: generate a question, given the input context

**Parameters**:
* `context`: related context, input sequence as a string
* `model_name`: choices:`AnonymousSub/SciFive_MedQuAD_question_generation`, others are possible
* returns a string as the generated question

`get_med_question(context, model_name)`: similar with `get_question(context, model_name)`.

`get_layman_text(text, model_name, min_length, max_length)`: translate the clinical text into layman understandable text
**Parameters**:
* `text`: input text string
* `model_name`: we provide our finetuned models: `ireneli1024/bigbird-pegasus-large-pubmed-plos-finetuned`,`ireneli1024/biobart-v2-base-plos-finetuned`,`ireneli1024/biobart-v2-base-elife-finetuned`,`ireneli1024/bart-large-PLOS-finetuned`,`ireneli1024/bart-large-elife-finetuned`,`ireneli1024/bigbird-pegasus-large-pubmed-elife-finetuned`
* `min_length`: int, min length of the generated text
* `max_length`: int, max length of the generated text
* returns a string as the generated translated text


`get_dialogpt()`: an interactive function for simple chat functions, relying on `microsoft/DialoGPT-medium` mode. 


`get_choice(text, question, choices, num_labels, model_name)`: 

**Parameters**:
* `model_name`: we provide our fintuned models: `RUI525/ClinicalBERT-finetune-HEADQA`, `RUI525/BioBERT-finetune-HEADQA`, `RUI525/PubMedBERT-finetune-HEADQA`, `RUI525/SapBERT-finetune-HEADQA`, `RUI525/GatorTron-finetune-HEADQA`, `RUI525/ClinicalBERT-finetune-MedMCQA-wo-context`, `RUI525/BioBERT-finetune-MedMCQA-wo-context`, `RUI525/PubMedBERT-finetune-MedMCQA-wo-context`, `RUI525/SapBERT-finetune-MedMCQA-wo-context`, `RUI525/GatorTron-finetune-MedMCQA-wo-context`, `RUI525/ClinicalBERT-finetune-MedMCQA-w-context`, `RUI525/BioBERT-finetune-MedMCQA-w-context`, `RUI525/PubMedBERT-finetune-MedMCQA-w-context`, `RUI525/SapBERT-finetune-MedMCQA-w-context`, `RUI525/GatorTron-finetune-MedMCQA-w-context`. And you can also use other models that are applicable to multiple-choice tasks.
* `text`: string, input content related to the question.
* `question`: string, input a question.
* `choices`: a list of string, input all choices.
* `num_labels`: int, input the number of choices.
* returns the correct choice

`get_mT5_translation(text,target_language)`: TODO for qingcheng
**Parameters**:
* `model_name`: choices:`...`, please list all the possible models, if we have our own finetuned ones, also list them, thanks


### ✨stanza_functions.py
`get_denpendencies(text)`: dependency parsing result for the input `text` in string, this is a wrapper of the stanza library.


### ✨summarization_functions.py
`get_single_summary(text, model_name="t5-small", min_length=50, max_length=200)`: single document summarization.

**Parameters**:
* `text`: a string for the input text
* `model_name`: bert model name in string, now we support the following models: `bart-large-cnn`', '`t5-small`', '`t5-base`', '`t5-large`', '`t5-3b`', '`t5-11b` 
* `min_length`: min length in summary
* `max_length`: max length in summary
* returns a list of summarization in string

`get_multi_summary_joint(text, model_name="osama7/t5-summarization-multinews", min_length=50, max_length=200)`: multi-document summarization function. Join all the input documents as a long document, then do single document summarization.

**Parameters**:
* `text`: a list of document in string
* `model_name`: bert model name in string, now we support the following models: `bart-large-cnn`, `t5-small`, `t5-base`, `t5-large`, `t5-3b`', `t5-11b` 
* `min_length`: min length in summary
* `max_length`: max length in summary
* returns a list of summarization in string

`get_multi_summary_extractive_textRank(text,ratio=-0.1,words=0)`: Textrank method for multi-doc summarization.

**Parameters**:
* `text`: a list of string
* `ratio`: the ratio of summary (0-1.0)
* `words`: the number of words of summary, default is 50
* returns a string as the final summarization

### ✨medspacy_functions.py 

`get_word_tokenization(text)`: word tokenization using medspaCy package.

**Parameters**:
* `text`: input string text
* returns a list of token or word in string

`get_section_detection(text,rules)`: given a string as the input, extract sections, consisting of medical history, allergies, comments and so on.

**Parameters**:
* `text`: input string text
* `rule`: the personalized rules, a dictionary of string, i.e., {"category": "allergies"}, default is None
* returns a list of spacy Section object

`get_UMLS_match(text)`: match the UMLS concept for the input text.

**Parameters**:
* `text`: input string text
* returns a list of tuples, (entity_text, label, similarity, semtypes)



