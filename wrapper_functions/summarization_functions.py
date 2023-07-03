from transformers import pipeline
from summa.summarizer import summarize

def get_single_summary(text, model_name="t5-small", min_length=50, max_length=200):
    '''
    https://huggingface.co/transformers/v3.0.2/_modules/transformers/pipelines.html#SummarizationPipeline
    :param text: input sequence, a string or a list of string
    :param model_name: model_name: "bart-large-cnn", "t5-small", "t5-base", "t5-large", "t5-3b", "t5-11b" and "razent/SciFive-large-Pubmed_PMC", other models https://huggingface.co/models?sort=downloads&search=summarization
    :param min_length: min length in summary
    :param max_length: max length in summary
    :return: a list of string
    '''
    # choices: '`bart-large-cnn`', '`t5-small`', '`t5-base`', '`t5-large`', '`t5-3b`', '`t5-11b`'
    classifier = pipeline("summarization",model=model_name,tokenizer=model_name)
    res = classifier(text,min_length=min_length,max_length=max_length)
    final_summary = []
    for summary in res:
        final_summary.append(summary['summary_text'])
    return final_summary


def get_multi_summary_joint(text, model_name="osama7/t5-summarization-multinews", min_length=50, max_length=200):
    '''
    Join all the input documents as a long document, then do single document summarization
    :param text: input sequence, a string or a list of string
    :param model_name: model_name:  "bart-large-cnn", "t5-small", "t5-base", "t5-large", "t5-3b", "t5-11b" and "razent/SciFive-large-Pubmed_PMC", other models https://huggingface.co/models?sort=downloads&search=summarization
    :param min_length: min length in summary
    :param max_length: max length in summary
    :return: a list of string
    '''
    # choices: '`bart-large-cnn`', '`t5-small`', '`t5-base`', '`t5-large`', '`t5-3b`', '`t5-11b`'
    classifier = pipeline("summarization", model=model_name, tokenizer=model_name)
    text = ' '.join(text)
    res = classifier(text, min_length=min_length, max_length=max_length)
    final_summary = []
    for summary in res:
        final_summary.append(summary['summary_text'])
    return final_summary



def get_multi_summary_extractive_textRank(text,ratio=-0.1,words=0):
    '''
    Textrank method for multi-doc summarization
    :param text: a list of string
    :param ratio: the ratio of summary (0-1.0)
    :param words: the number of words of summary, default is 50
    :return: a string as the final summary
    
    Example for testing:
    >>text1 = 'Automatic summarization is the process of reducing a text document with a \
    computer program in order to create a summary that retains the most important points \
    of the original document. As the problem of information overload has grown, and as \
    the quantity of data has increased, so has interest in automatic summarization.'
    >>text2 = 'Technologies that can make a coherent summary take into account variables such as \
    length, writing style and syntax. An example of the use of summarization technology \
    is search engines such as Google. Document summarization is another.'
    >>print(get_multi_summary_extractive_textRank([text1,text2]))
    '''
    text = ' '.join(text)
    summ = None
    if ratio>0:
        summ = summarize(text, ratio=ratio)

    if words>0:
        summ = summarize(text, words=words)

    if summ is None:
        summ = summarize(text, words=50)

    return summ.replace('\n',' ')
