from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl

class SelectorRule(BaseModel):
    name: str = Field(..., description="Label for the extracted field")
    selector: str = Field(..., description="CSS selector")
    attribute: Optional[str] = Field(None, description="HTML attribute to extract, or empty for text content")

class ScrapeRequest(BaseModel):
    url: str
    preset: Optional[str] = "custom"
    rules: List[SelectorRule] = []
    follow_redirects: bool = True
    timeout: int = 15

class ScrapeResponse(BaseModel):
    url: str
    status_code: int
    elapsed_seconds: float
    total_items: int
    data: Dict[str, List[Any]]
    title: Optional[str] = None
