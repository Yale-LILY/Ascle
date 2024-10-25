#!/usr/bin/env python3
# -*- coding: utf-8 -*- #

# ------------------------------------------------------------------------------
#   Copyright (C) 2024 Li-lab
#   @Filename: base.py
#   @Author: Peng Wei
#   @Date: 2024-10-24
#   @Email: weipeng0715@gmail.com
#   @Description: 
# ------------------------------------------------------------------------------
import stanza
import spacy
import logging
from PyRuSH import RuSH
from ..core.base import BaseProcessor

class NLPProcessor(BaseProcessor):
    def __init__(self, config: ModelConfig, tool='stanza', config_path='conf/rush_rules.tsv'):
        super().__init__(config)
        self.tool = tool.lower()
        self.config_path = config_path

        if self.tool == 'stanza':
            stanza.download('en')
            self.nlp = stanza.Pipeline('en')
        elif self.tool == 'scispacy':
            self.nlp = spacy.load('en_core_sci_sm')
        elif self.tool == 'pyrush':
            self.rush = RuSH(self.config_path)
        else:
            raise ValueError(f"Unsupported tool: {tool}")

        logging.basicConfig(level=logging.INFO)
        logging.info(f"Initialized NLP Processor with tool: {self.tool}")

    def load_model(self):
        # Stanza and SciSpacy models are loaded during initialization
        pass

    def process(self, text: Union[str, List[str]]):
        if isinstance(text, list):
            return [self._process_single(t) for t in text]
        return self._process_single(text)

    def _process_single(self, text):
        if self.tool == 'stanza':
            return [sentence.text for sentence in self.nlp(text).sentences]
        elif self.tool == 'scispacy':
            doc = self.nlp(text)
            return [sentence.text for sentence in doc.sents]
        elif self.tool == 'pyrush':
            sentences = self.rush.segToSentenceSpans(text)
            return [text[s.start:s.end] for s in sentences]
        else:
            raise ValueError(f"Unsupported tool: {self.tool}")
