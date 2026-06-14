from sqlmodel import SQLModel, Field


class LinkDB(SQLModel, table=True):
    __tablename__ = "links"

    id: int = Field(default=None, primary_key=True)
    scraper_run_id: int = Field(foreign_key="scraper_runs.id", index=True)
    url: str = Field(index=True)
    normalized_url: str = Field(index=True)
    text: str = Field()