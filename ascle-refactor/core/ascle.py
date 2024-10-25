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


from typing import Optional, List, Dict
from .config import ModelConfig
from ..models.manager import ModelManager
from ..processors.text.nlp_processor import NLPProcessor

class Ascle:
    def __init__(self, config: Optional[dict] = None):
        self.config = ModelConfig(**(config or {}))
        self.model_manager = ModelManager()
        self._initialize_processors()

    def _initialize_processors(self):
        self.model_manager.register_model("stanza", NLPProcessor(self.config, tool='stanza'))
        self.model_manager.register_model("scispacy", NLPProcessor(self.config, tool='scispacy'))
        self.model_manager.register_model("pyrush", NLPProcessor(self.config, tool='pyrush'))

    def process_text(self, text: str, processors: Optional[List[str]] = None) -> Dict[str, List[str]]:
        results = {}
        processors = processors or ["stanza", "scispacy", "pyrush"]

        for processor_name in processors:
            processor = self.model_manager.get_model(processor_name)
            if processor:
                results[processor_name] = processor.process(text)

        return results

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

    def cleanup(self):
        self.model_manager.cleanup()
