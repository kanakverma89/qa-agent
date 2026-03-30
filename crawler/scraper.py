"""
scraper.py — Web page scraper for the QA Agent crawler.

Fetches a URL and extracts structured UI elements (inputs, buttons, links)
that are later passed to the AI layer to generate test cases.

Dependencies:
    requests    — HTTP client (like HttpClient in C#)
    BeautifulSoup (bs4) — HTML parser (like HtmlAgilityPack / XmlDocument in C#)
    urljoin     — resolves relative URLs against a base (like new Uri(base, relative) in C#)
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def scrape_website(url: str) -> dict | None:
    """
    Scrapes the given URL and returns a structured summary of its interactive elements.

    This is the entry point for the crawler module. It performs an HTTP GET,
    parses the HTML, and extracts inputs, buttons, links, and API endpoints —
    providing the raw material for AI-generated test cases.

    Args:
        url (str): The fully qualified URL to scrape (e.g. "https://example.com/login").

    Returns:
        dict: A dictionary with four keys:
            - "inputs"  (list[dict]): All <input> elements with type, name, placeholder, id.
            - "buttons" (list[dict]): All clickable buttons/submit inputs with text, type, id.
            - "links"   (list[dict]): Up to 50 anchor tags with their text and resolved href.
            - "apis"    (list[str]):  Hrefs that look like API endpoints (contain "/api/").
        None: If the request fails or an exception is raised.

    C# analogy:
        Equivalent to a static helper method returning a nullable
        Dictionary<string, object> populated via LINQ .Select() projections.
    """
    try:
        # Mimic a real browser to avoid bot-detection blocks (HTTP 403/429).
        # In C# this would be httpClient.DefaultRequestHeaders.Add("User-Agent", "...")
        headers = {"User-Agent": "Mozilla/5.0"}

        # Perform the HTTP GET. timeout=15 prevents hanging on slow/unresponsive servers.
        # Equivalent to: httpClient.GetAsync(url) with a CancellationToken timeout.
        response = requests.get(url, headers=headers, timeout=15)

        # Throw an exception for 4xx (client error) and 5xx (server error) status codes.
        # Equivalent to: if (!response.IsSuccessStatusCode) throw new HttpRequestException(...)
        response.raise_for_status()

        # Parse the raw HTML string into a traversable DOM tree.
        # "html.parser" is Python's built-in parser — no extra install needed.
        # Equivalent to: var doc = new HtmlDocument(); doc.LoadHtml(response.Content)
        soup = BeautifulSoup(response.text, "html.parser")

        # --- Extract <input> elements ---
        # List comprehension = C# LINQ .Select(tag => new { ... })
        # tag.get("attr", default) = tag.GetAttributeValue("attr", default) in HtmlAgilityPack
        inputs = [
            {
                "type": tag.get("type", "text"),          # input type (text, password, checkbox…)
                "name": tag.get("name", ""),              # form field name used in HTTP POST body
                "placeholder": tag.get("placeholder", ""),# hint text shown inside the field
                "id": tag.get("id", ""),                  # CSS/JS identifier
            }
            for tag in soup.find_all("input")             # find_all = QuerySelectorAll("input")
        ]

        # --- Extract clickable buttons ---
        # Matches both <button> tags and <input type="submit|button"> elements.
        # The lambda filters by the "type" attribute; None means the attribute is absent.
        buttons = [
            {
                "text": tag.get_text(strip=True),         # visible label text (strip removes whitespace)
                "type": tag.get("type", "button"),        # submit | button | reset
                "id": tag.get("id", ""),
            }
            for tag in soup.find_all(
                ["button", "input"],
                type=lambda t: t in ("submit", "button", None)  # filter: only clickable types
            )
        ]

        # --- Extract anchor links ---
        # href=True means only include <a> tags that actually have an href attribute.
        # urljoin resolves relative paths: urljoin("https://x.com", "/about") → "https://x.com/about"
        # Equivalent to: new Uri(new Uri(url), tag.href).ToString() in C#
        links = [
            {
                "text": tag.get_text(strip=True),
                "href": urljoin(url, tag.get("href", "")),  # always produces an absolute URL
            }
            for tag in soup.find_all("a", href=True)
        ]

        # --- Extract API endpoint hints ---
        # Filters the links list for hrefs that contain "/api/" — a heuristic to spot REST endpoints.
        # Equivalent to: links.Where(l => l.Href.Contains("/api/")).Select(l => l.Href)
        apis = [
            link["href"]
            for link in links
            if "/api/" in link.get("href", "")
        ]

        return {
            "inputs": inputs,
            "buttons": buttons,
            "links": links[:50],  # cap at 50 to avoid overloading the AI prompt with tokens
            "apis": apis,
        }

    except Exception as e:
        # Catch-all keeps the agent running even if a single URL fails.
        # In production you'd want more granular handling (requests.Timeout, HTTPError, etc.)
        print("Scraper Error:", e)
        return None
