import spacy
from scispacy.abbreviation import AbbreviationDetector
from scispacy.hyponym_detector import HyponymDetector
from scispacy.linking import EntityLinker
from negspacy.negation import Negex

def get_abbreviations(model, text):
    """
    returns a list of tuples in the form (abbreviation, expanded form), each element being a str
    """

    # logging
    print(f"Identifying abbrevations using {model}")
    partial_input = '\n'.join(text.split('\n')[:5])
    print(f"Input text (truncated): {partial_input}\n...")

    # abbreviation detection with scispacy
    nlp = spacy.load(model)
    nlp.add_pipe("abbreviation_detector")
    doc = nlp(text)
    abbreviations = [(abrv.text, abrv._.long_form.text) for abrv in doc._.abbreviations]

    return abbreviations

def get_hyponyms(model, text):
    """
    returns a list of tuples in the form (hearst_pattern, entity_1, entity_2, ...), each element being a str
    """

    # logging
    print(f"Extracting hyponyms using {model}")
    partial_input = '\n'.join(text.split('\n')[:5])
    print(f"Input text (truncated): {partial_input}\n...")

    # hyponym detection with scispacy
    nlp = spacy.load(model)
    nlp.add_pipe("hyponym_detector", last=True, config={"extended": True})
    doc = nlp(text)
    hearst_patterns = [tuple([str(element) for element in pattern]) for pattern in doc._.hearst_patterns]

    return hearst_patterns

def get_linked_entities(model, text):
    """
    returns a dictionary in the form {named entity: list of strings each describing one piece of linked information}
    """

    # logging
    print(f"Entity linking using {model}")
    partial_input = '\n'.join(text.split('\n')[:5])
    print(f"Input text (truncated): {partial_input}\n...")

    # entity linking with scispacy
    output = {}

    nlp = spacy.load(model)
    nlp.add_pipe("scispacy_linker", config={"resolve_abbreviations": True, "linker_name": "umls"})
    doc = nlp(text)

    ents = doc.ents
    linker = nlp.get_pipe("scispacy_linker")

    for entity in ents:
        cur = []
        for umls_ent in entity._.kb_ents:
            cur.append(str(linker.kb.cui_to_entity[umls_ent[0]]))
        output[entity] = cur

    return output

def get_named_entities(model, text):
    """
    returns a list of strings, each string is an identified named entity
    """

    # logging
    print(f"Extracting named entities using {model}")
    partial_input = '\n'.join(text.split('\n')[:5])
    print(f"Input text (truncated): {partial_input}\n...")

    # named recognition with scispacy
    nlp = spacy.load(model)
    doc = nlp(text)
    named_entities = [str(ent) for ent in doc.ents]

    return named_entities


def get_negation_entities(model, text):
    """
    returns a list of pairs, default model is "en_core_web_sm"
    Negspacy is a spaCy pipeline component that evaluates whether Named Entities are negated in text.
    Example:
    >> test = get_negation_entities("en_core_web_sm","She does not like Steve Jobs but likes Apple products.")
    >> print (test)
    [(True, 'Steve Jobs'), (False, 'Apple')]
    """

    # logging
    print(f"Extracting whether Named Entities are negated using {model}")
    partial_input = '\n'.join(text.split('\n')[:5])
    print(f"Input text (truncated): {partial_input}\n...")

    # named recognition with scispacy
    nlp = spacy.load(model)
    nlp.add_pipe("negex", config={"ent_types":["PERSON","ORG","NORP","GPE"]})
    doc = nlp(text)
    pairs = [(ent._.negex,ent.text) for ent in doc.ents]

    return pairs

def get_pos_tagging(model, text):
    """
    returns the pos tagging for the input text; 
    returns a list of tuples
    model: `en_core_sci_sm`, `en_core_sci_md`,`en_core_sci_scibert`,`en_core_sci_lg`,`en_ner_craft_md`,`en_ner_jnlpba_md`,`en_ner_bc5cdr_md`,`en_ner_bionlp13cg_md`
    Check more: https://allenai.github.io/scispacy/
    example: 
    >>get_pos_tagging("en_core_sci_sm",'The patient presented with a persistent cough and shortness of breath.')
    [(The, 'DET'), (patient, 'NOUN'), (presented, 'VERB'), (with, 'ADP'), (a, 'DET'), (persistent, 'ADJ'), (cough, 'NOUN'), (and, 'CCONJ'), (shortness, 'NOUN'), (of, 'ADP'), (breath, 'NOUN'), (., 'PUNCT')]
    """
    nlp = spacy.load(model)
    
    doc = nlp(text)
    predicted = []
    for token in doc:
        predicted.append((token,token.pos_))
    return predicted
    
    