import time
import logging
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from app.config.settings import settings
from app.models.scraper_run import ScraperStatus
from app.schemas.scraper_run import ScraperRunPayload, ScraperRunResult
from app.schemas.link import LinkCreate

class ScraperService:
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                      " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    def __init__(self):
        self.logger = logging.getLogger(f"app.{__name__}")
        self.logger.info("Scraper Service initialized")

    async def scrape_url(self, scraper_run: ScraperRunPayload) -> ScraperRunResult:
        start_time = time.perf_counter()
        html, status_code, error_message = await self.__fetch_html(scraper_run=scraper_run)
        response_time_ms = int((time.perf_counter() - start_time) * 1000)

        if error_message is not None:
            return ScraperRunResult(
                status=ScraperStatus.FAILED,
                http_status=status_code,
                response_time_ms=response_time_ms,
                follow_redirects=scraper_run.follow_redirects,
                error_message=error_message
            )

        soup = BeautifulSoup(html, "lxml")
        links = self.__extract_links(scraper_run.url, soup)

        return ScraperRunResult(
            status=ScraperStatus.SUCCESS,
            http_status=status_code,
            response_time_ms=response_time_ms,
            links=links
        )

    async def __fetch_html(self, scraper_run: ScraperRunPayload) -> tuple[str | None, int, str | None]:
        try:
            client_httpx_kwargs = {
                "headers": self.HEADERS,
                "follow_redirects": scraper_run.follow_redirects,
                "timeout": float(scraper_run.timeout),
                "trust_env": False
            }

            proxy_url = settings.https_proxy or settings.http_proxy
            if proxy_url:
                client_httpx_kwargs["proxy"] = proxy_url

            async with httpx.AsyncClient(**client_httpx_kwargs) as client:
                response = await client.get(scraper_run.url)
                response.raise_for_status()

                return response.text, response.status_code, None

        except httpx.TimeoutException:
            self.logger.warning(f"URL {scraper_run.url} timed out after {float(scraper_run.timeout)} seconds")
            return None, 408, "Connection timeout"

        except httpx.HTTPStatusError as e:
            self.logger.warning(f"URL {scraper_run.url} returned status code {e.response.status_code}")
            return None, e.response.status_code, f"HTTP Error: {e.response.status_code}"

        except httpx.RequestError as e:
            self.logger.warning(f"Request error for URL {scraper_run.url}: {str(e)}")
            return None, 0, f"Request failed: {str(e)}"

    def __extract_links(self, url: str, html: BeautifulSoup) -> list[LinkCreate]:
        links_seen = set()
        links = []

        self.logger.info(f"Extracting links from {url}")
        for tag in html.find_all("a", href=True):
            href = tag.get("href", "").strip()
            if not href or href.startswith(("#", "mailto:", "javascript:", "tel:")):
                continue

            absolute = urljoin(url, href)
            parsed = urlparse(absolute)
            if parsed.scheme not in ("http", "https"):
                continue

            normalized_url = parsed._replace(fragment="").geturl()
            if normalized_url in links_seen:
                continue

            links_seen.add(normalized_url)
            text = tag.get_text(strip=True)[:200]

            self.logger.info(f"Extracted link: {absolute} - {text}")
            links.append(LinkCreate(url=absolute, normalized_url=normalized_url, text=text))
        return links