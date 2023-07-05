import argparse
from PyRuSH import RuSH
import stanza
from get_text_from_csv import get_df, get_notes_single_row_id

def get_sents_pyrush(text):
    print("Segment into sentences using PyRuSH")
    rush = RuSH('conf/rush_rules.tsv')
    sentences = rush.segToSentenceSpans(text)
    return sentences

def get_sents_stanza(text):
    stanza.download('en')
    nlp = stanza.Pipeline(lang='en', processors='tokenize')
    sentences = [sentence.text for sentence in nlp(text).sentences]
    return sentences

def get_multiple_sents_stanza(texts):
    stanza.download('en')
    nlp = stanza.Pipeline(lang='en', processors='tokenize')
    sentences = [[sentence.text for sentence in nlp(text).sentences] for text in texts]
    return sentences

if __name__ == "__main__":
    # parse command line arguments
    parser = argparse.ArgumentParser(description='Identify named entities in MIMIC EVENTNOTES')
    parser.add_argument('--mimic_dir', default='../../../tutorials/data/mimic_data/', type=str, help='directory to mimic data')
    parser.add_argument('--row_id', default=178, type=int,  help='row id of text to be processed')
    parser.add_argument('--output_file', default='./output_segment_sentences.txt', type=str, help='output to save segmented sentences')
    parser.add_argument('--tool', default='stanza', type=str, help='Tool for segmentation: stanza or pyrush')

    args = parser.parse_args()
    mimic_dir = args.mimic_dir
    row_id = args.row_id
    output_file = args.output_file
    tool = args.tool
    print(f"Data file: {mimic_dir}NOTEEVENTS.csv")

    df = get_df(mimic_dir + 'NOTEEVENTS.csv')
    text = get_notes_single_row_id(df, row_id)
    
    if tool == 'pyrush':
        sents = get_sents_pyrush(text)
    elif tool == 'stanza':
        sents = get_sents_stanza(text)

    with open(output_file, 'w') as f:
        if tool == 'pyrush':
            for sent in sents:
                f.write(text[sent.begin:sent.end] + '\n')
        elif tool == 'stanza':
            output_str = '\n'.join(sents)
            f.write(output_str)
