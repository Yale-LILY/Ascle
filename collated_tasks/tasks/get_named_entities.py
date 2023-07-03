import argparse
import spacy
import scispacy
from utils.get_text_from_csv import get_df, get_notes_single_row_id 

def get_named_entities(model, text):
    print(f"Extracting named entities using {model}")
    partial_input = '\n'.join(text.split('\n')[:10])
    print(f"Input text (truncated): {partial_input}\n...")
    nlp = spacy.load(model)
    doc = nlp(text)
    ents = list(doc.ents)
    return ents

if __name__ == "__main__":
    # parse command line arguments
    parser = argparse.ArgumentParser(description='Identify named entities in MIMIC EVENTNOTES')
    parser.add_argument('--mimic_dir', default='../../tutorials/data/mimic_data/', type=str, help='directory to mimic data')
    parser.add_argument('--model', default='en_core_sci_sm', type=str, help='model for spacy')
    parser.add_argument('--row_id', default=178, type=int,  help='row id of text to be processed')
    parser.add_argument('--output_file', default='./output_named_entities.txt', type=str, help='output to save identified named entities')

    args = parser.parse_args()
    mimic_dir = args.mimic_dir
    model = args.model
    row_id = args.row_id
    output_file = args.output_file
    print(f"Data file: {mimic_dir}NOTEEVENTS.csv")

    df = get_df(mimic_dir + 'NOTEEVENTS.csv')
    text = get_notes_single_row_id(df, row_id)
    named_entities  = get_named_entities(model, text)
    #print(named_entities)

    with open(output_file, 'w') as f:
        f.write('\n'.join([str(ent) for ent in named_entities]))
    print(f"Named entities written to {args.output_file}")
