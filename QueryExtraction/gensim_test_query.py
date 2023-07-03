'''
Based on TextRank
https://radimrehurek.com/gensim_3.8.3/summarization/summariser.html
'''
import gensim
from gensim.summarization import keywords


def gensim_extract(test_free_text,ratio=0.3):
    result = keywords(test_free_text,ratio)
    return result.split('\n')




