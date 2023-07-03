import argparse
from transformers import MarianMTModel, MarianTokenizer
from utils.get_text_from_csv import get_df, get_notes_single_row_id

LANG_CODE = {'Malay_written_with_Latin': '>>zlm_Latn<<', 'Mauritian_Creole': '>>mfe<<', 'Haitian': '>>hat<<', 'Papiamento': '>>pap<<', 'Asturian': '>>ast<<',
             'Catalan': '>>cat<<', 'Indonesian': '>>ind<<', 'Galician': '>>glg<<', 'Walloon': '>>wln<<', 'Spanish': '>>spa<<', 
             'French': '>>fra<<', 'Romanian': '>>ron<<', 'Portuguese': '>>por<<', 'Italian': '>>ita<<', 'Occitan': '>>oci<<',
             'Aragonese': '>>arg<<', 'Minangkabau': '>>min<<'}

def get_translation(text, model_name, target_language):
    print(f'Translating medical note using {model_name}')
    partial_input = '\n'.join(text.split('\n')[:10])
    print(f"Input text (truncated): {partial_input}\n...")
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    # check supported languages of the selected model
    #support_languages = tokenizer.supported_language_codes
    model = MarianMTModel.from_pretrained(model_name)
    sents = [f'{LANG_CODE[target_language]} ' + t for t in text.split('\n')]
    translated = model.generate(**tokenizer(sents, return_tensors="pt", padding=True))
    translated = [tokenizer.decode(t, skip_special_tokens=True) for t in translated]
    return translated

if __name__ == "__main__":
    # parse command line arguments
    parser = argparse.ArgumentParser(description='Translate medical notes in MIMIC EVENTNOTES')
    parser.add_argument('--mimic_dir', default='../../tutorials/data/mimic_data/', type=str, help='directory to mimic data')
    #parser.add_argument('--model', default='Helsinki-NLP/opus-mt-en-roa', type=str, help='model for bert')
    parser.add_argument('--target_language', default='Spanish', type=str, help='target language of translation, default to Spanish')
    parser.add_argument('--row_id', default=178, type=int,  help='row id of text to be processed')
    parser.add_argument('--output_file', default='./output_translation.txt', type=str, help='output to save translated note')

    args = parser.parse_args()
    mimic_dir = args.mimic_dir
    # model = args.model
    model = 'Helsinki-NLP/opus-mt-en-ROMANCE'
    target_language = args.target_language
    row_id = args.row_id
    output_file = args.output_file

    print(f"Data file: {mimic_dir}NOTEEVENTS.csv")

    df = get_df(mimic_dir + 'NOTEEVENTS.csv')
    text = get_notes_single_row_id(df, row_id) 
        
    translated  = get_translation(text, model, target_language)

    with open(output_file, 'w') as f:
        f.write('Original:\n')
        f.write(text + '\n')
        f.write('Translated:\n')
        f.write('\n'.join(translated) + '\n')
    print(f"Original & translated records written to {args.output_file}")
