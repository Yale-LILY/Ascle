
from .spacy_test_query import pytextrank_extract
from .gensim_test_query import gensim_extract
from .rake_test_query import rake_extract
from .rakun_test_query import rakun_extract
from .yake_test_query import yake_extract
from .keybert_test_query import keybert_extract

# t1='''
# In the field of computer vision, researchers have repeatedly shown the value of transfer learning — pre-training a neural network model on a known task, for instance ImageNet, and then performing fine-tuning — using the trained neural network as the basis of a new purpose-specific model. In recent years, researchers have been showing that a similar technique can be useful in many natural language tasks.
# A different approach, which is also popular in NLP tasks and exemplified in the recent ELMo paper, is feature-based training. In this approach, a pre-trained neural network produces word embeddings which are then used as features in NLP models.
# How BERT works
# BERT makes use of Transformer, an attention mechanism that learns contextual relations between words (or sub-words) in a text. In its vanilla form, Transformer includes two separate mechanisms — an encoder that reads the text input and a decoder that produces a prediction for the task. Since BERT’s goal is to generate a language model, only the encoder mechanism is necessary. The detailed workings of Transformer are described in a paper by Google.
# As opposed to directional models, which read the text input sequentially (left-to-right or right-to-left), the Transformer encoder reads the entire sequence of words at once. Therefore it is considered bidirectional, though it would be more accurate to say that it’s non-directional. This characteristic allows the model to learn the context of a word based on all of its surroundings (left and right of the word).
# The chart below is a high-level description of the Transformer encoder. The input is a sequence of tokens, which are first embedded into vectors and then processed in the neural network. The output is a sequence of vectors of size H, in which each vector corresponds to an input token with the same index.
# When training language models, there is a challenge of defining a prediction goal. Many models predict the next word in a sequence (e.g. “The child came home from ___”), a directional approach which inherently limits context learning. To overcome this challenge, BERT uses two training strategies:
# Masked LM (MLM)
# Before feeding word sequences into BERT, 15% of the words in each sequence are replaced with a [MASK] token. The model then attempts to predict the original value of the masked words, based on the context provided by the other, non-masked, words in the sequence. In technical terms, the prediction of the output words requires:
# Adding a classification layer on top of the encoder output.
# Multiplying the output vectors by the embedding matrix, transforming them into the vocabulary dimension.
# Calculating the probability of each word in the vocabulary with softmax.
#
# '''
#
# my_list1 = ['computer vision', 'bert', 'transformer', 'neural network', 'imagenet', 'Masked LM',
#            'embedding matrix','softmax']



def evaluate(list, my_list1):

    count = 0
    for kw in list:
        if kw in my_list1:
            count+=1

    return count

def main_extraction(words_search, text):
    t1 = text
    print ('Extraction:')

    print ('SpaCy TextRank:')
    extracted = pytextrank_extract(t1,30)
    print ('Captured ',evaluate(extracted, words_search))
    print (extracted)
    print ('-'*30)

    print ('Gensim TextRank:')
    extracted = gensim_extract(t1,0.3)
    print ('Captured ',evaluate(extracted, words_search))
    print (extracted)
    print ('-'*30)

    print ('Rake:')
    extracted = rake_extract(t1,30)
    print ('Captured ',evaluate(extracted, words_search))
    print (extracted)
    print ('-' * 30)

    print ('Rakun:')
    extracted = rakun_extract(t1)
    print ('Captured ',evaluate(extracted, words_search))
    print (extracted)
    print ('-' * 30)


    print ('Yake:')
    extracted = yake_extract(t1)
    print ('Captured ',evaluate(extracted, words_search))
    print (extracted)
    print ('-' * 30)


    print ('KeyBERT:')
    extracted = keybert_extract(t1)
    print ('Captured ',evaluate(extracted, words_search))
    print (extracted)