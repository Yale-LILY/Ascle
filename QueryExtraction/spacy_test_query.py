'''
test
'''

import json
import spacy
import pytextrank
from collections import defaultdict




nlp = spacy.load('en_core_web_sm')

# load
nlp = spacy.load("en_core_web_sm")
# add PyTextRank to the spaCy pipeline
tr = pytextrank.TextRank()
nlp.add_pipe(tr.PipelineComponent, name='textrank', last=True)


# method
def pytextrank_extract(free_text,topk=30):
    query_set = defaultdict(float)

    'textrank extraction'
    doc = nlp(free_text)

    for p in doc._.phrases:

        if len(p.text) > 5:
            query_set[p.text] = query_set[p.text] + p.rank

    ordered_query_set = [(k,v) for k, v in sorted(query_set.items(), key=lambda item: item[1],reverse=True)][:topk]

    result_list = []
    for query, score in ordered_query_set:
        # print(query,score)
        result_list.append(query)
    return result_list


# ordered_query_set = extract(test_free_text)



#
# # print out
