'''
Date: 2023-06-30 10:38:23
LastEditors: Qingcheng Zeng
LastEditTime: 2023-06-30 11:57:59
FilePath: /Irene_Qingcheng/transformers_MT.py
'''
import transformers
from transformers import MT5Tokenizer,MT5ForConditionalGeneration

def get_mT5_translation(text,target_language):
    """
    This function generates a translated text from English to target language
    using multilingual T5.
    """
    lang_code = {"French":"fr","Polish":"pl","German":"de","Romanian":"ro",
                 "Hungarian":"hu","Spanish":"es","Swedish":"sv","Czech":"cs"}
    reversed_code = {"fr":"French","pl":"Polish","de":"German","ro":"Romanian",
                     "hu":"Hungarian","es":"Spanish","sv":"Swedish","cs":"Czech"}
    full_name = list(lang_code.keys())
    abbrev_name = list(lang_code.values())
    assert target_language in full_name or target_language in abbrev_name

    if target_language in full_name:
        target_language = lang_code[target_language]
    
    model_name = "qcz/en-{}-UFAL-medical".format(target_language)
    model = MT5ForConditionalGeneration.from_pretrained(model_name)
    tokenizer = MT5Tokenizer.from_pretrained(model_name)

    prefix = "translate English to {}: ".format(reversed_code[target_language])
    input_ids = tokenizer(prefix+text,return_tensors="pt")["input_ids"]
    generated_ids = model.generate(input_ids, max_new_tokens=512)
    prediction = tokenizer.decode(generated_ids[0], skip_special_tokens=True)

    return prediction