from app.models.url import UrlDB
from app.models.scraper_run import ScraperRunDB
from app.models.history import HistoryDB

def test_get_history_empty(client):
    response = client.get("/api/v1/history/")

    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["pagination"]["total"] == 0
    assert data["pagination"]["has_next"] is False


def test_get_history_with_data(client, session):
    db_url = UrlDB(url="https://test.com", normalized_url="https://test.com")
    session.add(db_url)
    session.commit()

    db_run = ScraperRunDB(
        url_id=db_url.id,
        status="SUCCESS",
        http_status=200,
        response_time_ms=150,
        follow_redirects=True
    )
    session.add(db_run)
    session.commit()

    db_history = HistoryDB(url_id=db_url.id, scraper_run_id=db_run.id)
    session.add(db_history)
    session.commit()

    response = client.get("/api/v1/history/")
    assert response.status_code == 200
    data = response.json()

    assert data["pagination"]["total"] == 1
    assert data["pagination"]["has_next"] is False

    assert len(data["items"]) == 1
    item = data["items"][0]
    assert item["url"]["url"] == "https://test.com"
    assert item["scraper_run"]["status"] == "SUCCESS"

def test_get_history_by_id_success(client, session):
    db_url = UrlDB(url="https://test2.com", normalized_url="https://test2.com")
    session.add(db_url)
    session.commit()

    db_run = ScraperRunDB(
        url_id=db_url.id,
        status="FAILED",
        http_status=404,
        response_time_ms=50,
        follow_redirects=True
    )
    session.add(db_run)
    session.commit()

    db_history = HistoryDB(url_id=db_url.id, scraper_run_id=db_run.id)
    session.add(db_history)
    session.commit()

    response = client.get(f"/api/v1/history/{db_history.id}/")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == db_history.id
    assert data["url"]["url"] == "https://test2.com"

def test_get_history_by_url_id_success_multiple_runs(client, session):
    db_url = UrlDB(url="http://test3.com", normalized_url="http://test3.com")
    session.add(db_url)
    session.commit()

    scraper_run_1 = ScraperRunDB(
        url_id=db_url.id,
        status="FAILED",
        http_status=0,
        response_time_ms=401,
        follow_redirects=True,
        error_message="Error 1"
    )

    scraper_run_2 = ScraperRunDB(
        url_id=db_url.id,
        status="SUCCESS",
        http_status=200,
        response_time_ms=150,
        follow_redirects=True
    )
    session.add_all([scraper_run_1, scraper_run_2])
    session.commit()

    history_1 = HistoryDB(url_id=db_url.id, scraper_run_id=scraper_run_1.id)
    history_2 = HistoryDB(url_id=db_url.id, scraper_run_id=scraper_run_2.id)
    session.add_all([history_1, history_2])
    session.commit()

    response = client.get(f"/api/v1/history/url-id/{db_url.id}/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2

    assert data[0]["url"]["url"] == "http://test3.com"
    assert data[1]["url"]["url"] == "http://test3.com"

    statuses = [item["scraper_run"]["status"] for item in data]
    assert "FAILED" in statuses
    assert "SUCCESS" in statuses


def test_get_history_by_id_not_found(client):
    response = client.get("/api/v1/history/9999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "History with id 9999 not found"

def test_get_history_by_url_id_not_found(client):
    response = client.get("/api/v1/history/url-id/9999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "History with URL id 9999 not found"

def test_get_history_by_scraper_id_not_found(client):
    response = client.get("/api/v1/history/scraper-run-id/9999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "History with Scraper run id 9999 not found"