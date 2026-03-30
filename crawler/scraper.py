import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def scrape_website(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        inputs = [
            {
                "type": tag.get("type", "text"),
                "name": tag.get("name", ""),
                "placeholder": tag.get("placeholder", ""),
                "id": tag.get("id", ""),
            }
            for tag in soup.find_all("input")
        ]

        buttons = [
            {
                "text": tag.get_text(strip=True),
                "type": tag.get("type", "button"),
                "id": tag.get("id", ""),
            }
            for tag in soup.find_all(["button", "input"], type=lambda t: t in ("submit", "button", None))
        ]

        links = [
            {
                "text": tag.get_text(strip=True),
                "href": urljoin(url, tag.get("href", "")),
            }
            for tag in soup.find_all("a", href=True)
        ]

        # Extract any API-like hrefs (paths containing /api/)
        apis = [
            link["href"]
            for link in links
            if "/api/" in link.get("href", "")
        ]

        return {
            "inputs": inputs,
            "buttons": buttons,
            "links": links[:50],  # limit to avoid token overflow
            "apis": apis,
        }

    except Exception as e:
        print("Scraper Error:", e)
        return None
