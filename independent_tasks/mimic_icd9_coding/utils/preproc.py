#%%
import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import RegexpTokenizer, stopwords
from nltk.stem.snowball import SnowballStemmer

def remove_special_chars(data):
    #replace special characers in notes
    #Create a unicode character dictionary
    special_chars = {'¶':' ', 'Þ': ' ', 'Û':' '}
    data.replace(special_chars, regex=True, inplace=True)
    # return data.replace(special_chars)
    return data


def lowercase_tokenizer(data, no_sentences):
    tokenizer = RegexpTokenizer(r'\w+')
    if no_sentences:
        data = data.apply(lambda x: tokenizer.tokenize(x.lower()))
    else:
        data = data.apply(lambda a: [[tokenizer.tokenize(x.lower()) for x in d] for d in a])
    return data



def main_preproc_row(text):
    """ With a single piece of text as input, run every preprocessing step defined above"""
    raise NotImplementedError

def main_preproc_series(data, stemming=True, no_punct=False, no_sentences=True, stop_words=True):
    """ With input series of text, run every preprocessing step defined above"""

    data = data.astype(str)

    # remove special characters
    data = remove_special_chars(data)

    # seperate sentences -- consider not doing this because sentences maybe not common
    if not no_sentences:
        data = data.apply(sent_tokenize)

    # # remove empty rows
    # data = data[data.map(lambda d: len(d)) > 0]

    # convert everything to lowercase and tokenize
    data = lowercase_tokenizer(data, no_sentences)

    # Remove numbers (and later names)
    data = data.apply(lambda x: [s for s in x if s.isalpha()])

    # filter out punctuation
    if no_punct:
       data = data.apply(lambda l: filter(lambda x: x not in string.punctuation, l))

    # filter out stop words -- note: removes haven, we can remove with other names etc.
    if stop_words:
        stop_words = stopwords.words('english')
        data = data.apply(lambda l: list(filter(lambda x: x not in stop_words, l)))

    #preform stemming
    if stemming:
        stemmer = SnowballStemmer("english", ignore_stopwords=True)
        data = data.apply(lambda x: [stemmer.stem(a) for a in x])

    return data


def bert_preproc(data):
    """ With input row of text, run every preprocessing step defined above"""
    """Note that by making this a row, we just call the preproc with apply"""
    # data = data.astype(str)

    # remove special characters
    data = remove_special_chars(data)

    # seperate sentences -- consider not doing this because sentences maybe not common
    data = sent_tokenize(data)

    # # remove empty rows
    # data = data[data.map(lambda d: len(d)) > 0]

    # convert everything to lowercase and tokenize
    # data = lowercase_tokenizer(data, no_sentences)

    # Remove numbers (and later names)
    # data = data.apply(lambda x: [s for s in x if s.isalpha()])

    # filter out punctuation
    # if no_punct:
    #    data = data.apply(lambda l: filter(lambda x: x not in string.punctuation, l))

    # filter out stop words -- note: removes haven, we can remove with other names etc.
    # if stop_words:
        # stop_words = stopwords.words('english')
        # data = data.apply(lambda l: list(filter(lambda x: x not in stop_words, l)))

    #preform stemming
    # if stemming:
        # stemmer = SnowballStemmer("english", ignore_stopwords=True)
        # data = data.apply(lambda x: [stemmer.stem(a) for a in x])

    return data

# %%
# %%
#Filter out some POS that we are not interested in 
# filtered_words = {key: value for (key, value) in word_count.items() if nltk.pos_tag([key])[0][1] not in ['CC', 'IN', 'DT', 'CD']}

#%% 
def demo():
    import pandas as pd
    folder_path = "/home/br384/project/prot_data/"
    data_path = folder_path + "evaluation_data.xlsx"
    df = pd.read_excel(data_path, 'Notes1')
    data = df['NOTE TEXT']
    return main_preproc_series(data)
