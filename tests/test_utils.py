import pytest

from src.football_pipeline.utils import sanitize_url


@pytest.mark.parametrize(
    "input_url, expected_result",
    [
        ("example_com", "example_com"),
        ("example.com", "example_com"),
        ("example.com/page1", "example_com_page1"),
        ("example.com/", "example_com"),
        ("http://example.com", "example_com"),
        ("https://example.com", "example_com"),
        ("Xwww.example.com", "X_example_com"),
        ("www.example.com", "example_com"),
        ("wwwexample.com", "wwwexample_com"),
        (r"exa&`~%mple.com", "exa____mple_com"),
        ("https://www.google.com/", "google_com"),
    ],
    ids=[
        "given already correct format, then expect no change",
        "given single dot, convert dot to underscore",
        "given forward slash not at end, convert forward to underscore",
        "given forward slash at end, then strip underscore so not present",
        "given http://, then remove http:// but do not add underscore",
        "given https://, then remove https:// but do not add underscore",
        "given www. not at start, then convert to single underscore",
        "given www. at start, then do not include the underscore",
        "given www without dot, then do not convert to underscore",
        "given non letter or digit characters, convert all to underscore",
        "given https://www., then remove this leading part and do not add underscore",
    ],
)
def test_sanitize_url(input_url, expected_result):
    result = sanitize_url(input_url)
    assert result == expected_result
