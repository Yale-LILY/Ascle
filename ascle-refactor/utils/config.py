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

from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class ModelConfig:
    name: str
    device: str = "cpu"
    max_length: int = 512
    batch_size: int = 32

@dataclass
class ProcessingConfig:
    cache_dir: str = ".cache"
    num_workers: int = 4
    use_gpu: bool = False

class AscleConfig:
    def __init__(self, **kwargs):
        self.model_config = ModelConfig(**kwargs.get("model", {}))
        self.processing_config = ProcessingConfig(**kwargs.get("processing", {}))
