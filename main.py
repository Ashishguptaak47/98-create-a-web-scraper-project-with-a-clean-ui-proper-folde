from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from scraper.models import ScrapeRequest, ScrapeResponse
from scraper.engine import scrape_target
import uvicorn

app = FastAPI(title="Web Scraper Studio", version="1.0.0")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/scrape", response_model=ScrapeResponse)
async def api_scrape(request: ScrapeRequest):
    try:
        result = await scrape_target(request)
        return result
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Failed to scrape target: {str(exc)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
