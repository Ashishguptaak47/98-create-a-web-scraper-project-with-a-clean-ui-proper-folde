import time
from typing import Dict, List, Any
import httpx
from bs4 import BeautifulSoup
from .models import ScrapeRequest, ScrapeResponse, SelectorRule

PRESETS: Dict[str, List[SelectorRule]] = {
    "articles": [
        SelectorRule(name="Headings (H1-H2)", selector="h1, h2"),
        SelectorRule(name="Paragraphs", selector="p"),
        SelectorRule(name="Links", selector="a[href]", attribute="href"),
    ],
    "media": [
        SelectorRule(name="Images", selector="img[src]", attribute="src"),
        SelectorRule(name="Image Alt", selector="img[alt]", attribute="alt"),
    ],
    "seo": [
        SelectorRule(name="Meta Description", selector="meta[name='description']", attribute="content"),
        SelectorRule(name="Canonical", selector="link[rel='canonical']", attribute="href"),
        SelectorRule(name="OpenGraph Title", selector="meta[property='og:title']", attribute="content"),
        SelectorRule(name="OpenGraph Image", selector="meta[property='og:image']", attribute="content"),
    ],
}

async def scrape_target(req: ScrapeRequest) -> ScrapeResponse:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) WebScraperStudio/1.0"
    }
    start = time.perf_counter()
    async with httpx.AsyncClient(follow_redirects=req.follow_redirects, timeout=req.timeout) as client:
        resp = await client.get(req.url, headers=headers)
    elapsed = round(time.perf_counter() - start, 3)

    soup = BeautifulSoup(resp.text, "html.parser")
    page_title = soup.title.string.strip() if soup.title and soup.title.string else None

    rules = req.rules
    if req.preset in PRESETS:
        rules = PRESETS[req.preset] + req.rules

    extracted: Dict[str, List[Any]] = {}
    total_items = 0

    for rule in rules:
        values = []
        for el in soup.select(rule.selector):
            if rule.attribute:
                val = el.get(rule.attribute, "")
                if isinstance(val, list):
                    val = " ".join(val)
            else:
                val = el.get_text(separator=" ", strip=True)
            if val:
                values.append(val)
        extracted[rule.name] = values
        total_items += len(values)

    return ScrapeResponse(
        url=str(resp.url),
        status_code=resp.status_code,
        elapsed_seconds=elapsed,
        total_items=total_items,
        data=extracted,
        title=page_title,
    )
