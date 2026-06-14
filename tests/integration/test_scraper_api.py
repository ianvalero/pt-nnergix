def test_extract_links_real(client):
    payload = {
        "url": "https://example.com",
        "follow_redirects": True,
        "timeout": 10.0
    }

    response = client.post("/api/v1/scraper/", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert "id" in data
    assert data["url"]["url"] == payload["url"]
    assert data["scraper_run"]["status"] == "SUCCESS"
    assert data["scraper_run"]["http_status"] == 200

    links = data["scraper_run"]["links"]
    assert len(links) == 1

    extracted_links = [link["url"] for link in links]
    assert "https://iana.org/domains/example" in extracted_links


def test_extract_links_domain_not_found(client):
    payload = {
        "url": "https://this-domain-not-exist.com",
        "follow_redirects": True,
        "timeout": 10.0
    }

    response = client.post("/api/v1/scraper/", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["url"]["url"] == payload["url"]

    scraper_run = data["scraper_run"]
    assert scraper_run["status"] == "FAILED"
    assert scraper_run["http_status"] == 0
    assert len(scraper_run["links"]) == 0
    assert "Request failed" in scraper_run["error_message"]

def test_extract_links_timeout(client):
    payload = {
        "url": "https://example.com",
        "follow_redirects": True,
        "timeout": 0.001
    }

    response = client.post("/api/v1/scraper/", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["url"]["url"] == payload["url"]

    scraper_run = data["scraper_run"]
    assert scraper_run["status"] == "FAILED"
    assert scraper_run["http_status"] == 408
    assert scraper_run["error_message"] == "Connection timeout"
    assert len(scraper_run["links"]) == 0