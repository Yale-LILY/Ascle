## Summarization of PubMed Articles

### Datasets
- We train the model on the medical research papers in the [Open Access Subset of the PubMed Central Corpus](https://www.ncbi.nlm.nih.gov/pmc/tools/openftlist/). 
- We can apply the trained model to the EHRs in the Medical Information Mart for Intensive Care ([MIMIC](https://mimic.physionet.org/gettingstarted/access/)) database.

### Extractive Summarization with Naive Bayes
Running pubmed_naive_bayes.py performs Naive Bayes summarization on the parsed Pubmed articles. To fit this model, feature vectors are constructed the first time it is run for a given number of articles and body type (see below). When the number of articles is large, this can take several hours. In this case, we recommend running pubmed_naive_bayes.py in a separate Linux screen.
```
> python pubmed_naive_bayes.py
Number of examples for training set: 500
Train with articles' whole body sections or just their body introductions? [w=whole body, j=just intro]: j
Training using the introduction of Pubmed articles.

Training Accuracy of Random Guessing: 62.9%
Training Accuracy of Model: 69.0%

Test Accuracy of Random Guessing: 61.6%
Model Average Test Accuracy: 65.2%

                                Model           Random Guessing
ROUGE-1 Average Precision:      0.526           0.532
ROUGE-1 Average Recall:         0.641           0.532
ROUGE-1 Average F1 Score:       0.573           0.528
--------------------
ROUGE-2 Average Precision:      0.409           0.373
ROUGE-2 Average Recall:         0.495           0.372
ROUGE-2 Average F1 Score:       0.445           0.37
--------------------
ROUGE-L Average Precision:      0.53            0.48
ROUGE-L Average Recall:         0.582           0.507
ROUGE-L Average F1 Score:       0.55            0.49

```
This creates a new directory, /PATH/TO/EHRKIT/summarization/pubmed_summarization/N_exs_BODY_TYPE/. This contains files with the articles selected for training and test sets. Inside this, the directory nb/ contains the feature vectors (feature_vecs.json and test_json/), as well as the model's predicted summaries (test_summaries/) and their ROUGE scores (ROUGE.txt) on the test set.

**get_pubmed_data.py** is called by **pubmed_naive_bayes.py** to build the feature vectors. Each feature vector represents one sentence, taking into account its number of nouns, its length, the average frequency of its words in the document, and the inverse sentence frequency. (Inverse sentence frequency measures the average importance of the words to that particular sentence relative to the document in general.) The sentence's label is 1 when it is in the abstract, and 0 otherwise.

Test 7.1 (t7.test7_1_naive_bayes) in **/tests/tests.py/** applies a trained Naive Bayes summarization model on an EHR in MIMIC. 

**demo.py** in **/demos/demo.py/** applies this trained Naive Bayes summarization model on EHRs in MIMIC and allows it to be called independently on any random text. See the Jupyter notebook in **/tutorials/** for more information on how to use this model. 

## Troubleshooting 
If you run into any errors running the Naive Bayes model, make sure to install bs4 and rouge. It might also be necessary to downloand 'stopwords' and 'averaged_perceptron_tagger' from the nltk library. 

