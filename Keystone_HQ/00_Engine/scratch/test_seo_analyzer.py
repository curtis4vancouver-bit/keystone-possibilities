import pytest
import sys
import os

# Add dynamic_skills path to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dynamic_skills import seo_analyzer

def test_calculate_keyword_density_case_0():
    input_args = {'text': 'Wayne Stevenson General Contractor Squamish local Squamish builder', 'target_word': 'Squamish'}
    res = seo_analyzer.calculate_keyword_density(**input_args)
    assert isinstance(res, dict)
    assert 'density' in res
    assert 'count' in res
    assert 'total_words' in res
    assert res.get('count') == 2
