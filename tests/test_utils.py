from string import punctuation

from hypothesis import given
from hypothesis import strategies as st

from src.football_pipeline.utils import sanitize_url


@given(st.text())
def test_sanitize_url(input_url):
    result = sanitize_url(input_url)
    invalid_substrings = [
        "https://",
        "http://",
        "www.",
    ] + [character for character in punctuation if character != "_"]
    assert all([substring not in result for substring in invalid_substrings])
