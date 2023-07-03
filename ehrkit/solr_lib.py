import requests
import logging
logger = logging.getLogger(__name__)
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

def solr_escape(query: str) -> str:
    # These special Solr characters need to be escaped. We deal with some of them
    # "+ - && || ! ( ) { } [ ] ^ " ~ * ? : \ /"
    char_translation_table = str.maketrans({
        '[': '',
        ']': '',
        '{': '',
        '}': '',
        '^': '',
        '~': '',
        '*': '',
        '\\': '',
        '/': '',
        '"': '',
        '!': '\!',
        '?': '\?',
        ':': '\:',
    })
    return query.translate(char_translation_table)

def get_solr_response_generic(solr_formatted_query: str, solr_core_name: str):
    solr_response_json = requests.get(
        url ='http://tangra.cs.yale.edu:8983/solr/{}/select?'.format(solr_core_name),
        params={
            'indent': 'on',
            'q': solr_formatted_query,
            'rows': '100',
            'wt': 'json',
            'fl': 'id, score'
        }
    ).json()
    solr_response = solr_response_json['response']
    num_rows = solr_response['numFound']
    rows = solr_response['docs']
    solr_matched_ids = []
    id_to_score_map = {}
    for row in rows:
        item_id = int(row['id'])
        item_solr_score = float(row['score'])
        solr_matched_ids.append(item_id)
        id_to_score_map[item_id] = item_solr_score

    return solr_matched_ids, id_to_score_map
def get_solr_response_mimic(raw_query):
    escaped_query = solr_escape(raw_query)
    query_words = ['"' + lemmatizer.lemmatize(word) + '"' for word in escaped_query.split()]
    if len(query_words) > 0:
            query = ' AND '.join(query_words)
            solr_formatted_query = 'abbreviations:({}) OR abbreviations_sent_id:({}) OR doctext_not_stored:({})'.format(
                query, query, query)
    else:
        solr_formatted_query = '*:*'

    return get_solr_response_generic(solr_formatted_query, 'ehr_abbs_mimic')
def get_solr_response_umn_wrap(raw_query):
    escaped_query = solr_escape(raw_query)
    query_words = ['"' + lemmatizer.lemmatize(word) + '"' for word in escaped_query.split()]
    if len(query_words) > 0:
            query = ' AND '.join(query_words)
            solr_formatted_query = 'short_form:({})'.format(
                query)
    else:
        solr_formatted_query = '*:*'

    return get_solr_response_umn(solr_formatted_query, 'ehr_abbsense_umn')

def get_solr_response_umn(solr_formatted_query: str, solr_core_name: str):
    solr_response_json = requests.get(
        url ='http://tangra.cs.yale.edu:8983/solr/{}/select?'.format(solr_core_name),
        params={
            'indent': 'on',
            'q': solr_formatted_query,
            'rows': '100',
            'wt': 'json',
            'fl': 'id, long_form, score'
        }
    ).json()
    solr_response = solr_response_json['response']
    num_rows = solr_response['numFound']
    rows = solr_response['docs']
    solr_matched_longforms = []
    long_form_to_score_map = {}
    for row in rows:
        item = row['long_form']
        item_solr_score = float(row['score'])
        solr_matched_longforms.append(item)
        long_form_to_score_map[item] = item_solr_score
    return solr_matched_longforms, long_form_to_score_map
