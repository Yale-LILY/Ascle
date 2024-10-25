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


import medspacy
from typing import List, Dict, Any
from ..core.base import BaseProcessor

class MedspacyProcessor(BaseProcessor):
    def load_model(self):
        self._model = medspacy.load(enable=["sentencizer", "quickumls"])
        return self._model

    def process(self, text: str) -> Dict[str, Any]:
        if self._model is None:
            self.load_model()
        
        doc = self._model(text)
        
        return {
            "entities": [(ent.text, ent.label_) for ent in doc.ents],
            "sections": [(sec.category, sec.title_span.text) for sec in doc._.sections],
        }
