from sklearn.cluster import KMeans
import argparse
from get_text_from_csv import get_df, get_notes_row_id
from get_representations import get_bert_embeddings
import stanza
import pandas as pd

if __name__ == '__main__':
    # parse command line arguments
    parser = argparse.ArgumentParser(description='Cluster medical notes in MIMIC EVENTNOTES')
    parser.add_argument('--mimic_dir', default='../../../tutorials/data/mimic_data/', type=str, help='directory to mimic data')
    parser.add_argument('--model', default='microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract', type=str, help='model for bert')
    parser.add_argument('--k', default=2, type=int, help='number of clusters')
    parser.add_argument('--row_ids', nargs='+', default=[174, 178, 2500, 3000], type=int, help='list of row_ids')
    parser.add_argument('--output_file', default='output_clustering.csv', type=str, help='output to save clustering information')

    args = parser.parse_args()
    mimic_dir = args.mimic_dir
    model = args.model
    k = args.k
    row_ids = args.row_ids
    output_file = args.output_file

    df = get_df(mimic_dir + 'NOTEEVENTS.csv')
    notes = get_notes_row_id(df, row_ids)
    # tokenize into sentences usng stanza
    stanza.download('en')
    nlp = stanza.Pipeline(lang='en', processors='tokenize')
    tokenized_texts = [[sentence.text for sentence in nlp(note).sentences] for note in notes]

    encoded_texts = get_bert_embeddings(model, tokenized_texts)
    #print(encoded_texts[:2])

    kmeans = KMeans(n_clusters=k)
    kmeans.fit(encoded_texts)
    labels = kmeans.labels_
    output_df = pd.DataFrame(list(zip(notes, labels)), columns=['note', 'cluster'])
    output_df.to_csv(output_file, index=False)
