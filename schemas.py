from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class URLRequest(BaseModel):
    original_url: str
    custom_short_url: Optional[str] = None  # Custom short URL
    expiration_date: Optional[datetime] = None  # Expiration date for the shortened URL

class URLResponse(BaseModel):
    original_url: str
    short_url: str
    access_count: int  # Track the number of accesses
    expiration_date: Optional[datetime] = None

    class Config:
        orm_mode = True
