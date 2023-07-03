'''
https://github.com/MaartenGr/KeyBERT

Other choices: xlm-r-distilroberta-base-paraphrase-v1

Cite:
@misc{grootendorst2020keybert,
  author       = {Maarten Grootendorst},
  title        = {KeyBERT: Minimal keyword extraction with BERT.},
  year         = 2020,
  publisher    = {Zenodo},
  version      = {v0.1.3},
  doi          = {10.5281/zenodo.4461265},
  url          = {https://doi.org/10.5281/zenodo.4461265}
}

'''

from keybert import KeyBERT


def keybert_extract(doc,topk=30):
    '''
    Return 1-gram,2-gram and 3-gram, return top 30
    :param doc:
    :param topk:
    :return:
    '''
    model = KeyBERT('distilbert-base-nli-mean-tokens')

    results = model.extract_keywords(doc, keyphrase_ngram_range=(1, 2), top_n=100,
                                     use_mmr=True, diversity=0.7,
                                     stop_words='english')

    selected = [k for k, v in sorted(results, key=lambda item: item[1], reverse=True)][:topk]

    return selected
