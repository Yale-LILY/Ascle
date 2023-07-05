import argparse
import numpy as np
from get_text_from_csv import get_df, get_notes_row_id 
from sklearn.feature_extraction.text import CountVectorizer
from transformers import AutoTokenizer, AutoModel
import torch

def get_bag_of_words(corpus):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(corpus)
    X = X.toarray()
    return X

def get_bert_embeddings(pretrained_model, texts):
    tokenizer = AutoTokenizer.from_pretrained(pretrained_model)
    model = AutoModel.from_pretrained(pretrained_model, return_dict=False, output_hidden_states=True)
    output_embeddings = []
    for text in texts:
        # print(len(text))
        # get emebeddings for each sentence, compute mean to represent document
        inputs = tokenizer(text, padding=True, truncation=True, max_length=128, return_tensors='pt')
        with torch.no_grad():
            model_output = model(**inputs)
        pooled_output = model_output[1]
        # print(pooled_output.shape) # (num_sentences, 768)
        # print(pooled_output)
        mean_embedding = torch.mean(pooled_output, axis=0)
        # print(mean_embedding.shape)
        output_embeddings.append(mean_embedding.numpy())
    return output_embeddings

if __name__ == "__main__":
    # parse command line arguments
    parser = argparse.ArgumentParser(description='Vectorize notes in MIMIC EVENTNOTES')
    parser.add_argument('--mimic_dir', default='../../../tutorials/data/mimic_data/', type=str, help='directory to mimic data')
    parser.add_argument('--row_ids', nargs='+', default=[174,178,2500,3000], type=list,help='row ids of text to be processed')
    parser.add_argument('--output_file', default='./output_vectors', type=str, help='output to save identified named entities')

    args = parser.parse_args()
    mimic_dir = args.mimic_dir
    row_ids = args.row_ids
    output_file = args.output_file
    print(f"Data file: {mimic_dir}NOTEEVENTS.csv")

    df = get_df(mimic_dir + 'NOTEEVENTS.csv')
    docs = get_notes_row_id(df, row_ids)
    X = get_bag_of_words(docs)
    print(X)
    # save to file for further tasks
    #np.save(output_file, X)
