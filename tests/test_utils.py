from string import punctuation

from hypothesis import given
from hypothesis import strategies as st

from src.football_pipeline.utils import sanitize_url


@given(st.text())
def test_sanitize_url(input_url):
    result = sanitize_url(input_url)
    assert "." not in result
    assert "https://" not in result
    assert "http://" not in result
    assert "www." not in result
    assert punctuation not in result
