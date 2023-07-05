import argparse
import numpy as np
import pandas as pd
from get_text_from_csv import get_df, get_notes_row_id, get_notes_single_row_id
from get_representations import get_bert_embeddings
from get_sentences import get_sents_stanza, get_multiple_sents_stanza
from sklearn.metrics.pairwise import cosine_similarity

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find similar documents in MIMIC EVENTNOTES')
    parser.add_argument('--mimic_dir', default='../../../tutorials/data/mimic_data/', type=str, help='directory to mimic data')
    parser.add_argument('--representation', default='microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract', type=str, help='representation for text')
    parser.add_argument('--top_k', default=2, type=int, help='number similar documents to find')
    parser.add_argument('--doc_id', default=178, type=int, help='id of query document')
    parser.add_argument('--candidates', nargs='+', default=[174, 176, 180, 191], type=int, help='ids of candidate documents')
    parser.add_argument('--output_file', default='./output_similar_documents.csv', type=str, help='output to save top k similar documents')

    args = parser.parse_args()
    mimic_dir = args.mimic_dir
    representation = args.representation
    top_k = args.top_k
    doc_id = args.doc_id
    candidates = args.candidates
    output_file = args.output_file

    df = get_df(mimic_dir + 'NOTEEVENTS.csv')
    query_note = get_notes_single_row_id(df, doc_id)
    candidate_notes = get_notes_row_id(df, candidates)
    candidate_vectors = np.array(get_bert_embeddings(representation, get_multiple_sents_stanza(candidate_notes)))
    query_vector = get_bert_embeddings(representation, [get_sents_stanza(query_note)])
    # print(query_vector)
    # print(candidate_vectors)
    # compute cosine similarity
    similarities = cosine_similarity(query_vector, candidate_vectors)[0]
    print(similarities)
    sorted_args = np.argsort(similarities)[::-1]
    print(sorted_args)
    top_args = sorted_args[:top_k]
    selected_rows = np.array(candidates)[top_args]
    selected_similarities = np.array(similarities)[top_args]
    selected_texts = np.array(candidate_notes)[top_args]

    output_df = pd.DataFrame({'row_id': selected_rows, 'similarities': selected_similarities, 'texts': selected_texts})
    output_df.to_csv(output_file, index=False)
