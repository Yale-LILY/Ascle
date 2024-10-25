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
from abc import ABC, abstractmethod
from typing import List, Optional, Union


class BaseProcessor(ABC):
    def __init__(self, config: ModelConfig):
        self.config = config
        self._model = None
        self._tokenizer = None

    @abstractmethod
    def load_model(self):
        pass

    @abstractmethod
    def process(self, text: Union[str, List[str]]):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

    def cleanup(self):
        if hasattr(self, '_model'):
            del self._model

