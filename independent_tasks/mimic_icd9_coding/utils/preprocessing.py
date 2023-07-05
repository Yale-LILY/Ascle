import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import RegexpTokenizer, stopwords
from nltk.stem.snowball import SnowballStemmer
import string

def remove_special_chars(data):
    #replace special characers in notes
    #Create a unicode character dictionary
    special_chars = {'¶':' ', 'Þ': ' ', 'Û':' '}
    special_chars = {'__': ''}
    data.replace(special_chars, regex=True, inplace=True)
    return data


def lowercase_tokenizer(data, sentences):
    tokenizer = RegexpTokenizer(r'\w+')
    if sentences:
        data = data.map(lambda a: [[tokenizer.tokenize(x.lower()) for x in d] for d in a])
    else:
        data = data.map(lambda x: tokenizer.tokenize(x.lower()))
    return data



def main_preproc_row(text):
    """ With a single piece of text as input, run every preprocessing step defined above"""
    raise NotImplementedError

def main_preproc_series(data, tokenize = False, stemming=True, no_punct=True, sentences=False, stop_words=True):
    """ With input series of text, run every preprocessing step defined above"""

    data = data.astype(str)

    # remove special characters
    data = remove_special_chars(data)
    if not tokenize:
        return data.map(str.lower)
    # seperate sentences -- consider not doing this because sentences maybe not common
    if sentences:
        data = data.apply(sent_tokenize)
    else:
    # convert everything to lowercase and tokenize
        data = lowercase_tokenizer(data, sentences)

    # # remove empty rows
    # data = data[data.map(lambda d: len(d)) > 0]


    # Remove numbers (and later names)
    if sentences:
        data = data.apply(lambda x: [s for s in x if s.isalpha()])

    # filter out punctuation
    if no_punct:
       data = data.apply(lambda l: list(filter(lambda x: x not in string.punctuation, l)))

    # filter out stop words -- note: removes haven, we can remove with other names etc.
    if stop_words:
        stop_words = stopwords.words('english')
        data = data.apply(lambda l: list(filter(lambda x: x not in stop_words, l)))

    #preform stemming
    if stemming:
        stemmer = SnowballStemmer("english", ignore_stopwords=True)
        data = data.apply(lambda x: [stemmer.stem(a) for a in x])

    return data
    
def clean_data(text_series):
    """Main cleaning function for a series of text"""
    return main_preproc_series(text_series)