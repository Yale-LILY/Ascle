import stanza

def get_named_entities_stanza_biomed(text):
    """
    returns a list of tuples in the form (named entity, type), each being a str
    """
    stanza.download('en', package='mimic', processors={'ner': 'i2b2'})
    nlp = stanza.Pipeline('en', package='mimic', processors={'ner': 'i2b2'})
    doc = nlp(text)

    named_entities = [(ent.text, ent.type) for ent in  doc.entities]

    return named_entities

def get_sents_stanza_biomed(text):
    stanza.download('en', package='craft')
    nlp = stanza.Pipeline('en', package='craft')
    doc = nlp(text)

    sents = [sentence.text for sentence in doc.sentences]

    return sents

def get_tokens_stanza_biomed(text):
    stanza.download('en', package='craft')
    nlp = stanza.Pipeline('en', package='craft')
    doc = nlp(text)

    tokens = [[token.text for token in sentence.tokens] for sentence in doc.sentences]

    return tokens

def get_part_of_speech_and_morphological_features(text):
    """
    returns a list of lists of tuples of length 4: word, universal POS (UPOS) tags, treebank-specific POS (XPOS) tags,
    and universal morphological features (UFeats)
    """
    stanza.download('en', package='craft')
    nlp = stanza.Pipeline('en', package='craft')
    doc = nlp(text)

    tags = [[(word.text, word.upos, word.xpos, word.feats if word.feats else '_')
             for word in sent.words] for sent in doc.sentences]

    return tags

def get_lemmas_stanza_biomed(text):
    stanza.download('en', package='craft')
    nlp = stanza.Pipeline('en', package='craft')
    doc = nlp(text)

    lemmas = [[(word.text, word.lemma) for word in sent.words] for sent in doc.sentences]

    return lemmas

def get_dependency_stanza_biomed(text):
    """
    tuple of length 5:  word id, word text, head id, head text, deprel
    """

    stanza.download('en', package='craft')
    nlp = stanza.Pipeline('en', package='craft')
    doc = nlp(text)

    dependencies = [[(word.id, word.text, word.head, sent.words[word.head-1].text if word.head > 0 else "root", word.deprel)
                     for word in sent.words] for sent in doc.sentences ]

    return dependencies

def get_denpendencies(text):
    stanza.download('en', package='craft')
    nlp = stanza.Pipeline('en', package='craft')
    doc = nlp(text)
    dependencies = [sent.print_dependencies() for sent in doc.sentences]
    return dependencies