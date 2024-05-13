
# Ascle: we provide many off-shelf methods for processing medical text. 
[![Python 3.6.13](https://img.shields.io/badge/python-3.6.13-green.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.8.8](https://img.shields.io/badge/python-3.8.8-green.svg)](https://www.python.org/downloads/release/python-380/)
[![Python 3.8.16](https://img.shields.io/badge/python-3.8.16-green.svg)](https://www.python.org/downloads/release/python-380/)

## More examples
Here, we show examples of running a single-document task and a multi-document task. 

For a complete run-through of all tasks, run the demo script using ```python demo.py```. 

For a comprehensive tutorial, check the [tutorial notebook](https://github.com/Yale-LILY/Ascle/blob/v2.2/Ascle/Ascle_tutorials.ipynb).

### Single-document Task Example
Single document tasks operate on a single free-text record.

```python
from Ascle import Ascle

# create kit 
kit = Ascle()

main_record = "Spinal and bulbar muscular atrophy (SBMA) is an \
inherited motor neuron disease caused by the expansion \
of a polyglutamine tract within the androgen receptor (AR). \
SBMA can be caused by this easily."

# add main_record
kit.update_and_delete_main_record(main_record)

# call single-document tasks on main_record
kit.get_abbreviations()
>> [('SBMA', 'Spinal and bulbar muscular atrophy'),
    ('SBMA', 'Spinal and bulbar muscular atrophy'),
    ('AR', 'androgen receptor')]
```

### Multi-document Task Example
Multi-document tasks operate on several free-text records.

```python
from Ascle import Ascle

# create kit 
kit = Ascle()

''' A document about neuron.'''
record = "Neurons (also called neurones or nerve cells) are the fundamental units of the brain and nervous system, "
         "the cells responsible for receiving sensory input from the external world, for sending motor commands to "
         "our muscles, and for transforming and relaying the electrical signals at every step in between. More than "
         "that, their interactions define who we are as people. Having said that, our roughly 100 billion neurons do"
         " interact closely with other cell types, broadly classified as glia (these may actually outnumber neurons, "
         "although it’s not really known)."

''' A document about neural network. '''
cand1 = "A neural network is a series of algorithms that endeavors to recognize underlying relationships in a set of "
        "data through a process that mimics the way the human brain operates. In this sense, neural networks refer to "
        "systems of neurons, either organic or artificial in nature."

''' A document about aspirin. '''
cand2 = "Prescription aspirin is used to relieve the symptoms of rheumatoid arthritis (arthritis caused by swelling "
        "of the lining of the joints), osteoarthritis (arthritis caused by breakdown of the lining of the joints), "
        "systemic lupus erythematosus (condition in which the immune system attacks the joints and organs and causes "
        "pain and swelling) and certain other rheumatologic conditions (conditions in which the immune system "
        "attacks parts of the body)."

''' Another document about aspirin. '''
cand3 = "People can buy aspirin over the counter without a prescription. Everyday uses include relieving headache, "
        "reducing swelling, and reducing a fever. Taken daily, aspirin can lower the risk of cardiovascular events, "
        "such as a heart attack or stroke, in people with a high risk. Doctors may administer aspirin immediately"
        " after a heart attack to prevent further clots and heart tissue death."

# add main_record
kit.update_and_delete_main_record(record)

# add supporting_records
kit.replace_supporting_records([cand1, cand2, cand3])

# performs k-means clustering on the 4 documents
kit.get_clusters(k=2)

>> note
cluster
0
Neurons(also
called
neurones or ...
0
1
A
neural
netwrok is a
series
of...
0
2
Prescription
aspirin is used
to...
1
3
People
can
buy
aspirin
over
the...
1
```

### More examples
```python
# create kit 
kit = Ascle()

# example 1: basic NLP function - get abbreviation terms
# user-defined input text
main_record = """
              Spinal and bulbar muscular atrophy (SBMA) is an inherited 
              motor neuron disease caused by the expansion of a polyglutamine 
              tract within the androgen receptor.
              """
kit.update_and_delete_main_record(main_record)

# call the function
kit.get_abbreviations()

# following is the example output
""">> [('SBMA', 'Spinal and bulbar muscular atrophy')]"""


# example 2: generation function - Question Answering (Answer Generation)

# load model and tokenizer
base_model, adapter_model, load_8bit = "decapoda-research/llama-7b-hf", 
                                       "project-baize/baize-healthcare-lora-7B", 
                                       False
tokenizer, model, device = load_tokenizer_and_model(base_model, 
                                                    adapter_model, 
                                                    load_8bit)
                                                    
# setup parameters
max_length = 256
temperature = 1.0
top_p = 1.0
top_k = 30
max_context_length_tokens = 180

question = "What is myopia?"

# call the answer-generation function and print the output 
print(answer_generation(base_model, adapter_model, question, max_length, 
temperature, top_p, top_k, max_context_length_tokens).replace("\n[|Human|]",""))

# following is the example output
""">> Myopia, also known as nearsightedness, is a visual impairment 
   in which distant objects are blurred and close objects appear 
   clear. It is caused by the elongation of the eyeball, which 
   results in the cornea being too steeply angled."""

# example 3: generation function - Understandable Translation
main_record = """
              The patient presents with symptoms of acute bronchitis, 
              including cough, chest congestion, and mild fever. 
              Auscultation reveals coarse breath sounds and occasional 
              wheezing. Based on the clinical examination, a diagnosis 
              of acute bronchitis is made, and the patient is prescribed 
              a short course of bronchodilators and advised to rest and 
              stay hydrated.
              """
# choose the model
layman_model = "ireneli1024/bart-large-elife-finetuned"
kit.update_and_delete_main_record(content)

# call the understandable translation function and print the output
print(kit.get_layman_text(layman_model, min_length=20, max_length=70))

# following is the example output
""">> The patient presents with symptoms of acute bronchitis including 
   cough, chest congestion and mild fever. Auscultation reveals coarse 
   breath sounds and occasional wheezing. Based on these symptoms and 
   the patient's history of previous infections with the same condition, 
   the doctor decides that the patient is likely to have a cold or bronch."""

```

### Key Functions
- Abbreviation Detection & Expansion
- Hyponym Detection
- Entity Linking
- Named Entity Recognition
- Machine Translation
- Sentencizer
- Document clustering
- Similar Document Retrieval
- Word Tokenization
- Negation Detection
- Section Detection
- UMLS Concept Extraction
- Understandable Translation
- Question Answering
- Question Generation
- Interactive Chatting

### New Release Models - June, 2023

#### Machine Translation: 
We fine-tuned on the [UFAL data](https://ufal.mff.cuni.cz/ufal_medical_corpus) to support more languages, feel free to download the Transformer models [MT5-based](https://huggingface.co/qcz), more models Users can also be found [SciFive-based](https://huggingface.co/irenelizihui/scifive_ufal_MT_en_es/). 

#### Multiple-Choice Question Answering:
We fine-tuned BioBERT, ClinicalBERT, SapBERT, GatorTron-base, PubMedBERT using [HEAD-QA](https://huggingface.co/datasets/head_qa), [MedMCQA](https://huggingface.co/datasets/medmcqa) datasets, please feel free to download [our fine-tuned Transformer models](https://huggingface.co/RUI525).



## Troubleshooting 🔧

### `ModuleNotFoundError: No module named 'click._bashcomplete'`

You may have dependency confusion and have the wrong version of click installed. Try `pip install click==7.1.1`.

### The demo.py file outputs "Killed" with no error message.

Your computer does not have enough CPU/GPU/RAM to run this model so your kernel shut down the process because it was starved for resources.

### `TypeError: 'module' object is not callable`

For some reason the PyRuSH module does not behave the same on all machines. Try replacing the line `rush = RuSH('conf/rush_rules.tsv')` with `rush = RuSH.RuSH('conf/rush_rules.tsv')` in the `utils.py` file.

### `AttributeError: 'IntervalTree' object has no attribute 'search'`

Another dependency confusion error: try `pip install intervaltree==2.1.0`.

