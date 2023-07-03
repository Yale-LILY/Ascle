from PyRuSH import RuSH
import stanza
import scispacy
import spacy

def get_sents_pyrush(text):
    print("Segment into sentences using PyRuSH")
    rush = RuSH('conf/rush_rules.tsv')
    sentences = rush.segToSentenceSpans(text)
    return sentences

def get_sents_stanza(text):
    stanza.download('en')
    nlp = stanza.Pipeline(lang='en', processors='tokenize')
    sentences = [sentence.text for sentence in nlp(text).sentences]
    return sentences

def get_multiple_sents_stanza(texts):
    stanza.download('en')
    nlp = stanza.Pipeline(lang='en', processors='tokenize')
    sentences = [[sentence.text for sentence in nlp(text).sentences] for text in texts]
    return sentences

def get_sents_scispacy(text):
    nlp = spacy.load("en_core_sci_sm")
    doc = nlp(text)
    sentences = [sentence.text for sentence in doc.sents]
    return sentences