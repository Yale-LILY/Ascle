
# EHRKit-WF: we provide many off-shelf methods for processing medical text. 
[![Python 3.6.13](https://img.shields.io/badge/python-3.6.13-green.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.8.8](https://img.shields.io/badge/python-3.8.8-green.svg)](https://www.python.org/downloads/release/python-380/)
[![Python 3.8.16](https://img.shields.io/badge/python-3.8.16-green.svg)](https://www.python.org/downloads/release/python-380/)


## Overview
We integrate various text-processing tools, with a focus on the medical domain, into one single, user-friendly toolkit.

## Installation
### Create virtual environment

```bash
python3 -m venv virtenv/ 
source virtenv/bin/activate
```
### Install packages
```bash
pip install pip==21.3.1
pip install -U spacy
pip install scispacy
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.4.0/en_core_sci_sm-0.4.0.tar.gz
pip install pandas==1.1.5
pip install numpy==1.19.5
pip install transformers==4.12.3
pip install torch==1.10.0
pip install torchvision==0.11.1
pip install sentencepiece==0.1.96
pip install sklearn
pip install PyRuSH
pip install stanza==1.3.0
pip install ipywidgets
pip install ipykernel
pip install summa==1.2.0
pip install negspacy==1.0.2
pip install medspacy==0.2.0.0
wget https://github.com/jianlins/PyRuSH/raw/master/conf/rush_rules.tsv -P conf
```

Or using `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Quick Start
Here, we show examples of runnng a single-document task and a multi-document task. 

For a complete run-through of all tasks, run the demo script by using ```python demo.py```. 

For a comprehensive tutorial, check the [tutorial notebook](https://github.com/karenacorn99/LILY-EHRKit/blob/main/EHRKit_tutorials.ipynb).

### Single-document Task Example
Single document tasks operates on a single free-text record.
```python
from EHRKit import EHRkit

# create kit 
kit = EHRKit()

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
from EHRKit import EHRkit

# create kit 
kit = EHRKit()

''' A document about neuron.'''
record = "Neurons (also called neurones or nerve cells) are the fundamental units of the brain and nervous system, " \
         "the cells responsible for receiving sensory input from the external world, for sending motor commands to " \
         "our muscles, and for transforming and relaying the electrical signals at every step in between. More than " \
         "that, their interactions define who we are as people. Having said that, our roughly 100 billion neurons do" \
         " interact closely with other cell types, broadly classified as glia (these may actually outnumber neurons, " \
         "although it’s not really known)."
         
''' A document about neural network. '''
cand1 = "A neural network is a series of algorithms that endeavors to recognize underlying relationships in a set of " \
        "data through a process that mimics the way the human brain operates. In this sense, neural networks refer to " \
        "systems of neurons, either organic or artificial in nature."
        
''' A document about aspirin. '''
cand2 = "Prescription aspirin is used to relieve the symptoms of rheumatoid arthritis (arthritis caused by swelling " \
        "of the lining of the joints), osteoarthritis (arthritis caused by breakdown of the lining of the joints), " \
        "systemic lupus erythematosus (condition in which the immune system attacks the joints and organs and causes " \
        "pain and swelling) and certain other rheumatologic conditions (conditions in which the immune system " \
        "attacks parts of the body)."

''' Another document about aspirin. '''
cand3 = "People can buy aspirin over the counter without a prescription. Everyday uses include relieving headache, " \
        "reducing swelling, and reducing a fever. Taken daily, aspirin can lower the risk of cardiovascular events, " \
        "such as a heart attack or stroke, in people with a high risk. Doctors may administer aspirin immediately" \
        " after a heart attack to prevent further clots and heart tissue death."
        
# add main_record
kit.update_and_delete_main_record(record)

# add supporting_records
kit.replace_supporting_records([cand1, cand2, cand3])

# performs k-means clustering on the 4 documents
kit.get_clusters(k=2)

>>                                     note   cluster
   0  Neurons (also called neurones or ...    0
   1  A neural netwrok is a series of ...     0
   2  Prescription aspirin is used to ...     1
   3  People can buy aspirin over the ...     1
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



## Troubleshooting 🔧

### `ModuleNotFoundError: No module named 'click._bashcomplete'`

You may have dependency confusion and have the wrong version of click installed. Try `pip install click==7.1.1`.

### The demo.py file outputs "Killed" with no error message.

Your computer does not have enough CPU/GPU/RAM to run this model so your kernel shut down the process because it was starved for resources.

### `TypeError: 'module' object is not callable`

For some reason the PyRuSH module does not behave the same on all machines. Try replacing the line `rush = RuSH('conf/rush_rules.tsv')` with `rush = RuSH.RuSH('conf/rush_rules.tsv')` in the `utils.py` file.

### `AttributeError: 'IntervalTree' object has no attribute 'search'`

Another dependency confusion error: try `pip install intervaltree==2.1.0`.

