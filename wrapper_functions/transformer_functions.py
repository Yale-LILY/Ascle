from transformers import MarianMTModel, MarianTokenizer, AutoConfig, AutoModelForMultipleChoice, AutoTokenizer, AutoModel,AutoModelForCausalLM
import torch
import numpy as np
from utils import get_sents_stanza, get_multiple_sents_stanza
from transformers import pipeline
from flair.data import Sentence
from flair.models import SequenceTagger

LANG_CODE = {'Malay_written_with_Latin': '>>zlm_Latn<<', 'Mauritian_Creole': '>>mfe<<', 'Haitian': '>>hat<<',
             'Papiamento': '>>pap<<', 'Asturian': '>>ast<<', 'Catalan': '>>cat<<', 'Indonesian': '>>ind<<',
             'Galician': '>>glg<<', 'Walloon': '>>wln<<', 'Spanish': '>>spa<<', 'French': '>>fra<<',
             'Romanian': '>>ron<<', 'Portuguese': '>>por<<', 'Italian': '>>ita<<', 'Occitan': '>>oci<<',
             'Aragonese': '>>arg<<', 'Minangkabau': '>>min<<'}

def get_supported_translation_languages():
    return list(LANG_CODE.keys())

def get_translation(text, model_name, target_language):
    '''
    returns a string, which is the translated version of text
    '''

    # logging
    print(f'Translating medical note using {model_name}')
    partial_input = '\n'.join(text.split('\n')[:5])
    print(f"Input text (truncated): {partial_input}\n...")

    # translation using MarianMT
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)

    sents = [f'{LANG_CODE[target_language]} ' + sent for sent in get_sents_stanza(text)]

    translated = model.generate(**tokenizer(sents, return_tensors="pt", padding=True))
    translated = ' '.join([tokenizer.decode(t, skip_special_tokens=True) for t in translated])

    return translated

def get_bert_embeddings(pretrained_model, texts):
    """
    texts: a list of lists of sentences, each list is made up of sentences from the same document
    """

    tokenizer = AutoTokenizer.from_pretrained(pretrained_model)
    model = AutoModel.from_pretrained(pretrained_model, return_dict=False, output_hidden_states=True)

    output_embeddings = []

    for text in texts:
        # get embeddings for each sentence, compute mean to represent document
        inputs = tokenizer(text, padding=True, truncation=True, max_length=128, return_tensors='pt')

        with torch.no_grad():
            model_output = model(**inputs)

        pooled_output = model_output[1]
        mean_embedding = torch.mean(pooled_output, axis=0)

        output_embeddings.append(mean_embedding.numpy())

    return output_embeddings

def get_single_summary(text, model_name="t5-small", min_length=50, max_length=200):
    '''
    https://huggingface.co/transformers/v3.0.2/_modules/transformers/pipelines.html#SummarizationPipeline
    :param text: input sequence, a string or a list of string
    :param model_name: model_name: `bart-large-cnn`', '`t5-small`', '`t5-base`', '`t5-large`', '`t5-3b`', '`t5-11b`
    :param min_length: min length in summary
    :param max_length: max length in summary
    :return: summary string
    '''
    # choices: '`bart-large-cnn`', '`t5-small`', '`t5-base`', '`t5-large`', '`t5-3b`', '`t5-11b`'

    classifier = pipeline("summarization", model=model_name, tokenizer=model_name)
    res = classifier(text, min_length=min_length, max_length=max_length)
    final_summary = []

    for summary in res:
        final_summary.append(summary['summary_text'])

    final_summary = '\n\n'.join(final_summary)

    return final_summary

def get_multi_summary_joint(text, model_name="osama7/t5-summarization-multinews", min_length=50, max_length=200):
    '''
    Join all the input documents as a long document, then do single document summarization
    :param text: input sequence, a string or a list of string
    :param model_name: model_name: `bart-large-cnn`', '`t5-small`', '`t5-base`', '`t5-large`', '`t5-3b`', '`t5-11b`, other models https://huggingface.co/models?sort=downloads&search=summarization
    :param min_length: min length in summary
    :param max_length: max length in summary
    :return: summary string
    '''
    # choices: '`bart-large-cnn`', '`t5-small`', '`t5-base`', '`t5-large`', '`t5-3b`', '`t5-11b`'

    classifier = pipeline("summarization", model=model_name, tokenizer=model_name)
    text = ' '.join(text)
    res = classifier(text, min_length=min_length, max_length=max_length)
    final_summary = []

    for summary in res:
        final_summary.append(summary['summary_text'])

    final_summary = '\n\n'.join(final_summary)

    return final_summary
  
  
def get_span_answer(question, context,model_name="sultan/BioM-ELECTRA-Large-SQuAD2"):
    
    # choices:`sultan/BioM-ELECTRA-Large-SQuAD2`(tested), `deepset/roberta-base-squad2`, `AnonymousSub/SciFive_MedQuAD_question_generation`
    # result is a dictionary, i.e., {'score': 0.9190713763237, 'start': 34, 'end': 40, 'answer': 'Berlin'}; we return the answer token directly
    # for testing purpose: question='Where do I live?', context="My name is Wolfgang and I live in Berlin"

    bot =  pipeline(model=model_name)
    answer = bot(question=question, context=context)
    return answer['answer']
    
def get_question(context, model_name="AnonymousSub/SciFive_MedQuAD_question_generation"):
    # generate a question given the input content
    bot =  pipeline(model=model_name)
    question = bot(context)
    
    return question

# def get_choice(question, candicates, model="russab0/distilbert-qa"):
#     # multiple-choice-qa there is no fine-tuned version on headQA!, reference: https://huggingface.co/persiannlp/mbert-base-parsinlu-multiple-choice
#     # we return the answer directly
#
#     # from typing import List
#     # import torch
#     #
#
#     # model_name = "persiannlp/mbert-base-parsinlu-multiple-choice"
#     model_name = model
#     tokenizer = AutoTokenizer.from_pretrained(model_name)
#     config = AutoConfig.from_pretrained(model_name)
#     model = AutoModelForMultipleChoice.from_pretrained(model_name, config=config)
#
#     assert len(candicates) == 4, "you need four candidates"
#     choices_inputs = []
#     for c in candicates:
#         text_a = ""  # empty context
#         text_b = question + " " + c
#         inputs = tokenizer(
#             text_a,
#             text_b,
#             add_special_tokens=True,
#             max_length=128,
#             padding="max_length",
#             truncation=True,
#             return_overflowing_tokens=True,
#         )
#         choices_inputs.append(inputs)
#
#     input_ids = torch.LongTensor([x["input_ids"] for x in choices_inputs])
#     output = model(input_ids=input_ids)
#
#     print (question+' choose from:')
#     print (candicates)
#
#     return candicates[torch.argmax(output['logits'])]

def get_choice(question, choices, model_checkpoint="microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract-fulltext"):

    '''
    param question: input a question, the type of question should be a string
    param choices: input a list of all choices, the type of each choice should be a string
    param model_checkpoint: choose models you want to use, the default model is PubMedBERT
    return: choice
    ---------------------------------------------------------------------------------------
    example:
    question = "The excitatory postsynaptic potentials:"
    choices = ["They are all or nothing." ,
               "They are hyperpolarizing.",
               "They can be added.",
               "They spread long distances.",
               "They present a refractory period."]
    answer = get_choice(question, choices)
    print(answer)
    "They can be added."
    '''

    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
    config = AutoConfig.from_pretrained(model_checkpoint)
    model = AutoModelForMultipleChoice.from_pretrained(model_checkpoint, config=config)

    choice_inputs = []
    for choice in choices:
        text = question + " " + choice
        inputs = tokenizer(
            text,
            add_special_tokens=True,
            max_length=128,
            padding="max_length",
            truncation=True,
            return_overflowing_tokens=True,
        )
        choice_inputs.append(inputs)

        input_ids = torch.LongTensor([i["input_ids"] for i in choice_inputs])
        output = model(input_ids=input_ids)

    return choices[torch.argmax(output["logits"])]
    
def get_med_question(context, model_name="AnonymousSub/SciFive_MedQuAD_question_generation"):
    # generate a question given the input content
    bot =  pipeline("text2text-generation", model=model_name)
    question = bot(context)[0]
    question = question['generated_text']
    return question

def get_layman_text(text, model_name="ireneli1024/bart-large-elife-finetuned",min_length=50, max_length=200):
    '''
    https://huggingface.co/transformers/v3.0.2/_modules/transformers/pipelines.html#SummarizationPipeline
    :param text: input sequence, a string or a list of string
    :param model_name: model_name: `bart-large-cnn`', '`t5-small`', '`t5-base`', '`t5-large`', '`t5-3b`', '`t5-11b`
    :param min_length: min length in summary
    :param max_length: max length in summary
    :return: summary string
    '''
    classifier = pipeline("summarization", model=model_name, tokenizer=model_name,min_length=min_length, max_length=max_length)
    res = classifier(text)
    final_summary = []

    for summary in res:
        final_summary.append(summary['summary_text'])

    lay_summary = '\n\n'.join(final_summary)

    return lay_summary

def get_dialogpt():
    

    tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
    model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

    # Let's chat for 5 lines
    for step in range(5):
        # encode the new user input, add the eos_token and return a tensor in Pytorch
        new_user_input_ids = tokenizer.encode(input(">>  User:") + tokenizer.eos_token, return_tensors='pt')

        # append the new user input tokens to the chat history
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids

        # generated a response while limiting the total chat history to 1000 tokens, 
        chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

        # pretty print last ouput tokens from bot
        print("DialoGPT: {}".format(tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)))

def get_pos_tagging_hf(text,model_name="flair/pos-english"):
    '''
    pos tagging using a huggingface model, you need to install flair to run it
    :param text: input sequence, a string or a list of string
    :param model_name: default "flair/pos-english"
    :return: a list of token/pos tag with a score. 
    '''
    
    tagger = SequenceTagger.load(model_name)
    
     # make example sentence
    sentence = Sentence(text)

    # predict NER tags
    tagger.predict(sentence)
    res = sentence.annotation_layers['pos']
    predicted = []
    for item in res:
        predicted.append((item,item._value))
    return res

