import os
import shutil
import random
import sys
import nltk
from bs4 import BeautifulSoup


def parse_body(soup, whole_body):
    if whole_body:
        body_tags = soup.findAll('body')
    else:
        body_tags = soup.findAll('sec', {'id': 'Sec1'})
    if not body_tags:
        return None

    unclean_body = str(body_tags[0])
    soup_body = BeautifulSoup(unclean_body, 'html.parser')
    paragraphs = soup_body.findAll('p')
    body = ''
    for p in range(len(paragraphs)):
        # Removes reference tags and concatenates
        body += (paragraphs[p].getText() + '\n')
    return body


def parse_file(file_path, whole_body):
    # Reads file as string
    with open(file_path, 'r') as f:
        content = f.readlines()
        content = ''.join(content)

    # Prepares text for parsing
    soup = BeautifulSoup(content, features='html.parser')

    # Reads abstract as clean text
    ab_tag = soup.find('abstract')
    if not ab_tag:
        return None

    # Abstract usually 1 paragraph
    ab_paragraphs = ab_tag.findAll('p')
    abstract = ''
    for p in range(len(ab_paragraphs)):
        abstract += (ab_paragraphs[p].getText() + '\n')

    body = parse_body(soup, whole_body)
    if whole_body:
        return abstract, body, None
    else:
        return abstract, None, body


def remove_short_paragraphs(text, strip_newlines):
    if text:
        # Removes short paragraphs
        paragraphs = text.split('\n')
        good_pars = []
        for p in paragraphs:
            if len(p.split()) > 20:
                good_pars.append(p)
        if len(good_pars) > 0:
            if strip_newlines:
                clean_text = ''.join(good_pars) + '\n'
            else:
                clean_text = '\n'.join(good_pars) + '\n'
            return clean_text
    return None


def random_summary(PARSED_DIR, filename, tokenizer):
    abstract_path = os.path.join(PARSED_DIR, 'abstract', filename + '.tgt')
    merged_path = os.path.join(PARSED_DIR, 'merged', filename + '.mgd')
    with open(abstract_path, "r") as abstract:
        abs_text = abstract.read().replace("\n", ". ").replace("..", ". ")
    with open(merged_path, "r") as mgd:
        mgd_text = mgd.read().replace("\n", ". ").replace("..", ". ")
    # Fraction of article classified as summary
    pct_sum = len(abs_text) / len(mgd_text)

    # Classifies at random
    mgd_sents = tokenizer.tokenize(mgd_text)
    rand_sum = ''
    indices = random.sample(list(range(len(mgd_sents))), round(pct_sum * len(mgd_sents)))
    for i in range(len(mgd_sents)):
        if i in indices:
            rand_sum += mgd_sents[i]

    summary_path = os.path.join(PARSED_DIR, 'random_summary', filename + '.sum')
    with open(summary_path, 'w') as sum:
        sum.write(rand_sum + '\n')

def run_parser():
    print('newer version')
    XML_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'xml'))
    PARSED_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'parsed_articles'))
    # XML_DIR = '/data/corpora/pubmed_xml_subset/'
    # PARSED_DIR = '/data/corpora/pubmed_parsed/'
    print('Path to XML files: %s' % XML_DIR)
    print('Path to parsed PubMed files: %s' % PARSED_DIR)

    body_type = input('Parse the whole body section of each article or just the body introduction? '\
                        '[w=whole body, j=just intro]: ')
    if body_type == 'w':
        PARSED_DIR = os.path.join(PARSED_DIR, 'with_whole_bodies')
        whole_body = True
    elif body_type == 'j':
        PARSED_DIR = os.path.join(PARSED_DIR, 'with_just_intros')
        whole_body = False
    else:
        sys.exit('Error: Must input \'w\' or \'j.\'')

    os.makedirs(PARSED_DIR, exist_ok=True)
    os.makedirs(os.path.join(PARSED_DIR, 'abstract'), exist_ok=True)
    os.makedirs(os.path.join(PARSED_DIR, 'body'), exist_ok=True)
    os.makedirs(os.path.join(PARSED_DIR, 'merged'), exist_ok=True)
    os.makedirs(os.path.join(PARSED_DIR, 'random_summary'), exist_ok=True)

    n_files = input('Number of files to parse [press Enter to parse all]: ')
    if n_files == '':
        n_files = -1
    else:
        n_files = int(n_files)
    count = 0
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    skipped_files = 0
    for root, dirs, files in os.walk(XML_DIR, topdown=True):
        for file in files:
            if skipped_files % 10 == 0:
                print('skipped {} files'.format(skipped_files), end = '\r')
            if file.endswith('.nxml'):
                # Check if xml file has already been parsed
                file_path = os.path.join(root, file)
                filename = file[:-5]
                tgt_path = os.path.join(PARSED_DIR, 'abstract', filename + '.tgt')
                if os.path.exists(tgt_path):
                    continue
                else:
                    # Extracts text
                    contents = parse_file(file_path, whole_body)
                    if not contents:
                        continue
                    else:
                        abstract, body, intro = contents[0], contents[1], contents[2]
                        abstract = remove_short_paragraphs(abstract, strip_newlines=True)
                        body = remove_short_paragraphs(body, strip_newlines=False)
                        intro = remove_short_paragraphs(intro, strip_newlines=False)
                        if not abstract:
                            skipped_files += 1
                            continue
                        if whole_body and not body:
                            skipped_files += 1
                            continue
                        if not whole_body and not intro:
                            skipped_files += 1
                            continue

                        # Writes abstract, body, and both to files
                        src_path = os.path.join(PARSED_DIR, 'body', filename + '.src')
                        mgd_path = os.path.join(PARSED_DIR, 'merged', filename + '.mgd')
                        with open(tgt_path, 'w') as tgt:
                            tgt.write(abstract)
                        with open(src_path, 'w') as src:
                            src.write(body) if whole_body else src.write(intro)
                        with open(mgd_path, 'w') as mgd:
                            mgd.write(abstract + body) if whole_body else mgd.write(abstract + intro)

                        random_summary(PARSED_DIR, filename, tokenizer)

                        count += 1
                        if count % 100 == 0:
                            print('Number of files parsed: %d' % count)
                        if count == n_files:
                            break
        if count == n_files:
            break
    if os.path.exists('__pycache__'):
        shutil.rmtree('__pycache__')
    if count < n_files:
        print('Only %d files could be parsed.' % count)
    else:
        print('Successfully parsed %d files.' % count)

if __name__ == "__main__":
    run_parser()