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

from transformers import MT5ForConditionalGeneration, MT5Tokenizer

class TranslationProcessor(BaseProcessor):
    def load_model(self):
        self._tokenizer = MT5Tokenizer.from_pretrained(self.config.name)
        self._model = MT5ForConditionalGeneration.from_pretrained(self.config.name).to(self.config.device)

    def process(self, text: str, target_language: str):
        if not self._model or not self._tokenizer:
            self.load_model()
        input_ids = self._tokenizer(f"translate English to {target_language}: {text}", return_tensors="pt").input_ids.to(self.config.device)
        generated_ids = self._model.generate(input_ids, max_length=self.config.max_length)
        return self._tokenizer.decode(generated_ids[0], skip_special_tokens=True)
