from app.repositories.url_repository import UrlRepository

def test_normalize_url_removes_trailing_slash():
    raw_url = "https://example.com/path/"
    expected_normalized_url = "https://example.com/path"
    result = UrlRepository.normalize_url(raw_url)
    assert result == expected_normalized_url

def test_normalize_url_leaves_other_urls_unchanged():
    raw_url = "HTTPS://WWW.Google.COM/Path"
    expected_url = "https://www.google.com/Path"
    result = UrlRepository.normalize_url(raw_url)
    assert result == expected_url