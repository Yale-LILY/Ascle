import argparse
import spacy
import scispacy
from scispacy.hyponym_detector import HyponymDetector
from utils.get_text_from_csv import get_df, get_notes_single_row_id 

def get_hyponyms(model, text):
    print(f"Extracting hyponyms using {model}")
    partial_input = '\n'.join(text.split('\n')[:10])
    print(f"Input text (truncated): {partial_input}\n...")
    nlp = spacy.load(model)
    # add hyponym pipe to spacy pipeline
    nlp.add_pipe("hyponym_detector", last=True, config={"extended": True}) # passing extended=True to use extended hearst patterns
    doc = nlp(text)
    hearst_patterns = doc._.hearst_patterns
    return hearst_patterns

if __name__ == "__main__":
    # parse command line arguments
    parser = argparse.ArgumentParser(description='Detect hyponyms in MIMIC EVENTNOTES')
    parser.add_argument('--mimic_dir', default='../../tutorials/data/mimic_data/', type=str, help='directory to mimic data')
    parser.add_argument('--model', default='en_core_sci_sm', type=str, help='model for spacy')
    parser.add_argument('--row_id', default=178, type=int,  help='row id of text to be processed')
    parser.add_argument('--output_file', default='./output_hyponyms.txt', type=str, help='output to save identified hyponyms')

    args = parser.parse_args()
    mimic_dir = args.mimic_dir
    model = args.model
    row_id = args.row_id
    output_file = args.output_file
    print(f"Data file: {mimic_dir}NOTEEVENTS.csv")

    df = get_df(mimic_dir + 'NOTEEVENTS.csv')
    text = get_notes_single_row_id(df, row_id)
    hyponyms = get_hyponyms(model, text)

    with open(output_file, 'w') as f:
        for tup in hyponyms:
            f.write(tup[0] + '\n')
            f.write(str(tup[1]) + '\n')
    print(f"Hyponyms written to {args.output_file}")
    print("Note that not all records contain hyponyms, so output files may be empty.")
