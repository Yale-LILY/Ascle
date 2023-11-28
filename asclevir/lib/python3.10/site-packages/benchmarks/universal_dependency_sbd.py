#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import sendfile
import pysbd
import random
import pyconll

# random.seed(25)

def universal_gold_text_sentences(conllu_content):
    expected_sents = [sent.text.rstrip('"') for sent in conllu_content]
    # sentences_random_order
    # random.shuffle(expected_sents)
    return "\n".join(expected_sents), expected_sents

if __name__ == "__main__":
    conllu_content = pyconll.load_from_file('/Users/nipunsadvilkar/projects/Personal/UD_Marathi-UFAL/mr_ufal-ud-dev.conllu')
    # conllu_content = pyconll.load_from_file('/Users/nipunsadvilkar/projects/Personal/UD_English-EWT/en_ewt-ud-dev.conllu')
    # conllu_content = pyconll.load_from_file('/Users/nipunsadvilkar/projects/Personal/UD_Spanish-GSD/es_gsd-ud-dev.conllu')
    text, expected = universal_gold_text_sentences(conllu_content)
    # text = "\n".join([l.strip().strip('"') for l in open('en-ewt.txt').readlines()])
    expected = text.split('\n')
    # segmenter = pysbd.Segmenter(language="mr", clean=False, char_span=False)
    segmenter = pysbd.Segmenter(language="en", clean=False, char_span=False)
    # segmenter = pysbd.Segmenter(language="es", clean=False, char_span=False)
    segments = segmenter.segment(text)
    segments = [s.strip() for s in segments]
    # 38
    # print(text)
    # print(expected[:15])
    # print(segments[:15])
    # while len(expected) < len(segments):
    #     expected.append("")
    # while len(segments) < len(expected):
    #     segments.append("")

    for seg, exp in zip(segments, expected):
        if seg == exp:
            pass
            print(f'{repr(exp[:10])} === {repr(seg[:10])}')
        else:
            print(f'{repr(exp)} >>> {repr(seg)}')
            # break
    print(len(segments), len(expected))
    # assert expected == segments
    # print(text[:200])
    # print(expected[:15])
    # print(segments[:15])
    # print(text[:100])
    # with open('en-ewt-segments.txt', 'w') as f:
    #     for ind, sent in enumerate(segments):
    #         f.write(sent + '\n')
            # if ind == 10:
            #     break
