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



import spacy

class ModelManager:
    def __init__(self):
        self._models = {}
        self._current_device = "cuda" if spacy.prefer_gpu() else "cpu"

    def register_model(self, name: str, processor: BaseProcessor) -> None:
        self._models[name] = processor

    def get_model(self, name: str) -> Optional[BaseProcessor]:
        return self._models.get(name)

    def cleanup(self) -> None:
        for model in self._models.values():
            model.cleanup()
        self._models.clear()
