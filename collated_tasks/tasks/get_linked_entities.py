import argparse
import spacy
import scispacy
from scispacy.linking import EntityLinker
from utils.get_text_from_csv import get_df, get_notes_single_row_id

def get_linked_entities(model, text):
    print(f"Entity linking using {model}")
    partial_input = '\n'.join(text.split('\n')[:10])
    print(f"Input text (truncated): {partial_input}\n...")
    output = {}
    nlp = spacy.load(model)
    # add the entity linking pipe to spacy pipeline
    nlp.add_pipe("scispacy_linker", config={"resolve_abbreviations": True, "linker_name": "umls"})
    doc = nlp(text)
    # get named entities
    ents = doc.ents
    # each entity is linked to UMLS with a score
    linker = nlp.get_pipe("scispacy_linker")
    for entity in ents:
        cur = {}
        for umls_ent in entity._.kb_ents:
            cur[umls_ent] = linker.kb.cui_to_entity[umls_ent[0]]
        output[entity] = cur
    return output

if __name__ == "__main__":
    # parse command line arguments
    parser = argparse.ArgumentParser(description='Linking named entities in MIMIC EVENTNOTES')
    parser.add_argument('--mimic_dir', default='../../tutorials/data/mimic_data/', type=str, help='directory to mimic data')
    parser.add_argument('--model', default='en_core_sci_sm', type=str, help='model for spacy')
    parser.add_argument('--row_id', default=178, type=int,  help='row id of text to be processed')
    parser.add_argument('--output_file', default='./output_linked_entities.txt', type=str, help='output to save linked entities')

    args = parser.parse_args()
    mimic_dir = args.mimic_dir
    model = args.model
    row_id = args.row_id
    output_file = args.output_file
    print(f"Data file: {mimic_dir}NOTEEVENTS.csv")

    df = get_df(mimic_dir + 'NOTEEVENTS.csv')
    text = get_notes_single_row_id(df, row_id)
    linked_entities  = get_linked_entities(model, text)

    with open(output_file, 'w') as f:
        for entity, entity_dic in linked_entities.items():
            f.write(str(entity) + '\n')
            f.write('\n\n'.join([f"{k}\t{v}" for k, v in entity_dic.items()]))
            f.write('\n\n\n')
    print(f"Linked entities written to {args.output_file}")
