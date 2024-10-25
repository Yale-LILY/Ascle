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

from transformers import pipeline
from ..core.base import BaseProcessor

class SummarizationProcessor(BaseProcessor):
    def load_model(self):
        self._model = pipeline("summarization", model=self.config.name, device=0 if self.config.device == "cuda" else -1)

    def process(self, text: Union[str, List[str]]):
        if not self._model:
            self.load_model()
        return self._model(text, max_length=self.config.max_length, min_length=25, do_sample=False)
