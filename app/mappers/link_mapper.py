from app.schemas.link import LinkCreate
from app.models.link import LinkDB

def to_link_model(link: LinkCreate, scraper_run_id: int) -> LinkDB:
    return LinkDB(
        scraper_run_id=scraper_run_id,
        url=link.url,
        normalized_url=link.normalized_url,
        text=link.text
    )