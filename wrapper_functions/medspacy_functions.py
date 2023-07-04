# pip install medspacy==0.2.0.0


import spacy
import medspacy
from medspacy.util import DEFAULT_PIPENAMES
from medspacy.custom_tokenizer import create_medspacy_tokenizer
import medspacy
from medspacy.section_detection import Sectionizer
from medspacy.section_detection import SectionRule

import warnings
warnings.filterwarnings("ignore")



def get_word_tokenization(text):
    """
    returns a list of strings of tokenized word from a input string

    example:
    >> get_word_tokenization("'''Admission Date:  [**2573-5-30**] ")
    >> ['Admission', 'Date', ':', '[', '*', '*', '2573', '-', '5',...]
    """

    # logging
    print(f"Getting sentence tokenizer from medspaCy\n")

    nlp = spacy.blank("en")

    medspacy_tokenizer = create_medspacy_tokenizer(nlp)

    print(f"Input text (truncated): {text}\n...")
    results = list(medspacy_tokenizer(text))

    'filter out empty elements'
    tokenized = [element.text.strip() for element in results if len(element.text.strip()) > 0]

    return tokenized


def get_section_detection(text,rules=None):
    '''
    given a string as the input, extract sections, consisting of medical history, allergies, comments and so on
    :param text: a string
    :rules: the personalized rules, a dictionary of string, i.e., {"category": "allergies"}
    :return: a list of spacy Section object.


    Example usage:
    >> text1 = 'Past Medical History:
    pt has history of medical events
    Comments: some comment here

    Allergies: apple, seafood
    peanuts'

    >> get_section_detection(text1)
    >>
    CATEGORY.............. past_medical_history
    TITLE................. Past Medical History:
    PARENT................ None
    SECTION TEXT..........

    pt has history of medical events

    ----------------------
    CATEGORY.............. comments
    TITLE................. Comments:
    PARENT................ None
    SECTION TEXT..........
    some comment here


    ----------------------
    CATEGORY.............. allergies
    TITLE................. Allergies:
    PARENT................ None
    SECTION TEXT..........
    apple, seafood
    peanuts
    '''
    nlp = medspacy.load()
    sectionizer = Sectionizer(nlp, rules=None)
    pattern_dicts = [{"category": "past_medical_history", "literal": "Past Medical History:"},
                     {"category": "allergies", "literal": "Allergies:"},
                     {"category": "medical_assessment", "literal": "Medical Assessment:"},
                     {"category": "comment", "literal": "Comments:", "parents": ["past_medical_history", "allergies"]}]
    if rules is not None:
        # combine with personalized rule
        pattern_dicts.append(rules)
    patterns = [SectionRule.from_dict(pattern) for pattern in pattern_dicts]
    sectionizer.add(patterns)
    nlp.add_pipe("medspacy_sectionizer")
    doc = nlp(text)
    sections = []

    print(f"Getting section detection function from medspaCy\n")
    for section in doc._.sections:
        print("CATEGORY.............. {0}".format(section.category))
        print("TITLE................. {0}".format(section.title_span))
        if section.parent:
            print("PARENT................ {0}".format(section.parent.category))
        else:
            print("PARENT................ {0}".format(section.parent))
        print("SECTION TEXT..........\n{0}".format(section.body_span))
        print("----------------------")
        sections.append(section)

    return sections

def get_UMLS_match(text):

    '''
    Match the UMLS concept for the input text.
    :param text: a string
    :return: a list of tuples, (entity_text, label, similarity, semtypes)

    Example:
    >> concept_text = 'Decreased dipalmitoyllecithin content found in lung specimens'
    >> get_UMLS_match(concept_type)
    >>
    Entity text : dipalmitoyllecithin
    Label (UMLS CUI) : C0000039
    Similarity : 0.8888888888888888
    Semtypes : {'T119', 'T121'}
    '''

    medspacy_pipes = DEFAULT_PIPENAMES.copy()

    if 'medspacy_quickumls' not in medspacy_pipes:
        medspacy_pipes.add('medspacy_quickumls')


    nlp = medspacy.load(enable=medspacy_pipes)


    doc = nlp(text)

    umls = []

    print(f"Getting UMLS matching from medspaCy\n")
    for ent in doc.ents:
        print('Entity text : {}'.format(ent.text))
        print('Label (UMLS CUI) : {}'.format(ent.label_))
        print('Similarity : {}'.format(ent._.similarity))
        print('Semtypes : {}'.format(ent._.semtypes))
        umls.append((ent.text,ent.label_,ent._.similarity, ent._.semtypes))

    return umls



# example code
demo_text1 = '''Admission Date:  [**2573-5-30**]              Discharge Date:   [**2573-7-1**]

Date of Birth:  [**2498-8-19**]             Sex:   F

Service: SURGERY

Allergies:
Hydrochlorothiazide

Attending:[**First Name3 (LF) 1893**]
Chief Complaint:
Abdominal pain

Major Surgical or Invasive Procedure:
PICC line [**6-25**]
ERCP w/ sphincterotomy [**5-31**]


History of Present Illness:
74y female with type 2 dm and a recent stroke affecting her
speech, who presents with 2 days of abdominal pain. Imaging sh'''
get_word_tokenization(demo_text1)

demo_text2 = '''Past Medical History: 
pt has history of medical events
Comments: some comment here

Allergies: apple, seafood
peanuts
'''
get_section_detection(demo_text2)



demo_text3 = 'Decreased dipalmitoyllecithin content found in lung specimens'
get_UMLS_match(demo_text3)


