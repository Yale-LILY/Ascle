# Tasks on Medical Data
Developed by Keen (keen.you@yale.edu) Fall 2021
## /tasks
These tasks are included in the wrapper function subdirectory, check [here](https://github.com/IreneZihuiLi/EHRKit-LILY/tree/main/wrapper_functions) for more comprehensive usage descriptions.

The /tasks directory contains code for tasks that utilize MIMIC data. Tasks including named entity recognition, abbreviation detection, entity linking, hyponym detection, and translation. 

The /tasks/utils subdirectory contains helper functions for various tasks including selecting medical notes from csv file using row\_id or subject\_id, vectorize notes, and segmenting notes into sentences. Additional tasks including document clustering and retrieving similar documents.

## /non_mimic
The /non\_mimic directory contains tasks that utilize medical data that is not MIMIC. Tasks including de-identification, inference, and question answering.

## Getting Started with Collated Tasks
#### Clone repo & prepare data
```
git clone https://github.com/Yale-LILY/EHRKit.git --depth=1
cd EHRKit/
cd tutorials
mkdir data
mkdir data/mimic_data
cp /data/corpora/mimic/NOTEEVENTS.csv ./data/mimic_data/.
```
#### Create virtual environment
```
python3 -m venv task_virenv/
source task_virenv/bin/activate
```
#### Install packages
```
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
```
