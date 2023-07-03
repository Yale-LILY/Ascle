'''

https://github.com/csurfer/rake-nltk
https://towardsdatascience.com/extracting-keyphrases-from-text-rake-and-gensim-in-python-eefd0fad582f

Paper: Automatic Keyword Extraction from Individual Documents
easily applied to new domains, and operates well on multiple types of documents. And efficiency.
Method is based on frequency.

'''
from rake_nltk import Rake

# Uses stopwords for english from NLTK, and all puntuation characters by
# default
r = Rake()



# Extraction given the text.
# r.extract_keywords_from_text(test_free_text)

# Extraction given the list of strings where each string is a sentence.
# r.extract_keywords_from_sentences(<list of sentences>)

# To get keyword phrases ranked highest to lowest.
# r.get_ranked_phrases()

# To get keyword phrases ranked highest to lowest with scores.
# print (r.get_ranked_phrases_with_scores())


def rake_extract(test_free_text,topk=30):
    r.extract_keywords_from_text(test_free_text)
    results = r.get_ranked_phrases()[:topk]

    return results


