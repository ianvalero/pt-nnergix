from bs4 import BeautifulSoup
from app.services.scraper_service import ScraperService

def test_extract_links_empty_html():
    url = "https://example.com"
    html_content = "<html><body><h1>No links page</h1></body></html>"
    soup = BeautifulSoup(html_content, "lxml")

    result = ScraperService()._ScraperService__extract_links(url, soup)
    assert len(result) == 0
    assert result == []

def test_extract_links_invalid_and_ignored_links():
    url = "https://example.com"
    html_content = """
    <html>
        <body>
            <a href="mailto:test@test.com">Send mail</a>
            <a href="javascript:void(0);">Click</a>
            <a href="#seccion-2">Section 2</a>
            <a>Empty link</a>
        </body>
    </html>
    """
    soup = BeautifulSoup(html_content, "lxml")

    result = ScraperService()._ScraperService__extract_links(url, soup)
    assert len(result) == 0

def test_extract_links_valid_relative_links():
    url = "https://example.com"
    html_content = """
    <html>
        <body>
            <a href="/contacto">Contacto</a>
        </body>
    </html>
    """
    soup = BeautifulSoup(html_content, "lxml")

    result = ScraperService()._ScraperService__extract_links(url, soup)
    assert len(result) == 1
    assert result[0].url == "https://example.com/contacto"
    assert result[0].text == "Contacto"