import argparse
import spacy
from scispacy.abbreviation import AbbreviationDetector
from utils.get_text_from_csv import get_df, get_notes_single_row_id

def get_abbreviations(model, text):
    print(f"Identifying abbrevations using {model}")
    partial_input = '\n'.join(text.split('\n')[:10])
    print(f"Input text (truncated): {partial_input}\n...")
    nlp = spacy.load(model)
    # add the abbreviation pipe to spacy pipeline
    nlp.add_pipe("abbreviation_detector")
    doc = nlp(text)
    return doc._.abbreviations

if __name__ == "__main__":
    # parse command line arguments
    parser = argparse.ArgumentParser(description='Identify abbreviations in MIMIC EVENTNOTES')
    parser.add_argument('--mimic_dir', default='../../tutorials/data/mimic_data/', type=str, help='directory to mimic data')
    parser.add_argument('--model', default='en_core_sci_sm', type=str, help='model for spacy')
    parser.add_argument('--row_id', default=178, type=int,  help='row id of text to be processed')
    parser.add_argument('--output_file', default='./output_abbreviations.txt', type=str, help='output to save identified abbreviations')

    args = parser.parse_args()
    mimic_dir = args.mimic_dir
    model = args.model
    row_id = args.row_id
    output_file = args.output_file
    print(f"Data file: {mimic_dir}NOTEEVENTS.csv")

    df = get_df(mimic_dir + 'NOTEEVENTS.csv')
    text = get_notes_single_row_id(df, row_id)
    abbreviations  = get_abbreviations(model, text)

    with open(output_file, 'w') as f:
        f.write("Abbreviation" + "\t\t" + "Definition\n")
        for abrv in abbreviations:
            #f.write(f"{abrv} \t ({abrv.start}, {abrv.end}) {abrv._.long_form}")
            f.write(f"{abrv}\t\t{abrv._.long_form}\n")
    print(f"Abbreviations written to {args.output_file}")
