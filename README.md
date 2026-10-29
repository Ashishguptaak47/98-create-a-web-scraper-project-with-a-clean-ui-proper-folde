# Web Scraper Studio

A modern, responsive web scraper application featuring a clean UI, asynchronous scraping engine, selector presets, real-time result preview, and export capabilities (JSON & CSV).

## Features
- **Clean Web Interface**: Minimalist dashboard to configure scrapes and inspect parsed records.
- **Preset & Custom Extraction**: Extract titles, metadata, links, images, headings, or custom CSS selectors.
- **Robust Engine**: Asynchronous fetching via `httpx` with configurable user-agent and timeouts.
- **Exports**: Instant downloadable output in JSON and CSV formats.
- **REST API**: Fully scriptable endpoints for headless data collection.

## Quick Start

```bash
pip install -r requirements.txt
python main.py
```

Open your browser at `http://127.0.0.1:8000`.

## Testing

```bash
pytest
```
