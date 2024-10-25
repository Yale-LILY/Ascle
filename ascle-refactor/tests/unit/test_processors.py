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
import pytest
from ascle.core.ascle import Ascle
from ascle.core.config import ModelConfig
from ascle.processors.text.nlp_processor import NLPProcessor

# Updating tests to cover all added functionalities
def test_stanza_processor():
    config = ModelConfig(name='stanza', device='cpu')
    processor = NLPProcessor(config, tool='stanza')
    result = processor.process("This is a test. This is another sentence.")
    assert len(result) == 2
    assert result[0] == "This is a test."
    assert processor.get_tokens("This is a test.")
    assert processor.get_lemmas("This is a test.")


def test_scispacy_processor():
    config = ModelConfig(name='scispacy', device='cpu')
    processor = NLPProcessor(config, tool='scispacy')
    result = processor.process("The patient presents with acute respiratory symptoms.")
    assert len(result) > 0
    assert processor.get_dependencies("The patient presents with acute respiratory symptoms.")


def test_ascle_class():
    with Ascle() as ascle:
        result = ascle.process_text("Patient has a history of hypertension.", processors=["stanza"])
        assert "stanza" in result
        assert len(result["stanza"]) > 0


def test_summarization_processor():
    with Ascle() as ascle:
        result = ascle.process_text("The patient presents with acute respiratory symptoms. The doctor suggested staying at home.", processors=["summarization"])
        assert "summarization" in result
        assert len(result["summarization"]) > 0


def test_translation_processor():
    with Ascle() as ascle:
        result = ascle.process_text("The patient presents with acute respiratory symptoms.", processors=["translation"])
        assert "translation" in result
        assert isinstance(result["translation"], str)

