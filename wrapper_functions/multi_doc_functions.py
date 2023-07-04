from transformer_functions import get_bert_embeddings
from utils import get_sents_pyrush, get_multiple_sents_stanza, get_sents_stanza
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
from utils import get_multiple_sents_stanza

def get_similar_documents(bert_model, query_note, candidate_notes, candidates, top_k=2):
    """
    retrieve top_k documents in candidate_notes that are most similar to query_note
    returns a dataframe with candidate_note_id, similarity_score, and candidate_text
    """

    candidate_vectors = np.array(get_bert_embeddings(bert_model, get_multiple_sents_stanza(candidate_notes)))
    query_vector = get_bert_embeddings(bert_model, [get_sents_stanza(query_note)])

    # compute cosine similarity
    similarities = cosine_similarity(query_vector, candidate_vectors)[0]

    sorted_args = np.argsort(similarities)[::-1]
    top_args = sorted_args[:top_k]

    selected_rows = np.array(candidates)[top_args]
    selected_similarities = np.array(similarities)[top_args]
    selected_texts = np.array(candidate_notes)[top_args]

    output_df = pd.DataFrame({'candidate_id': selected_rows,
                              'similarity_score': selected_similarities,
                              'candidate_text': selected_texts})

    return output_df

def get_clusters(bert_model, notes, k=2):
    """
    performs k-means clustering with documents represented using pre-trained transformers
    returns a dataframe with 2 columns: note and assigned cluster id
    """

    # performs k-means clustering on notes
    tokenized_texts = get_multiple_sents_stanza(notes)
    encoded_texts = get_bert_embeddings(bert_model, tokenized_texts)

    kmeans = KMeans(n_clusters=k)
    kmeans.fit(encoded_texts)
    labels = kmeans.labels_

    output_df = pd.DataFrame(list(zip(notes, labels)), columns=['note', 'cluster'])

    return output_df