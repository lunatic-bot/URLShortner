from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class URLMapping(Base):
    __tablename__ = "url_mappings"
    
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, unique=True, index=True)
    short_url = Column(String, unique=True, index=True)
    expiration_date = Column(DateTime, nullable=True)  # Expiration date for the URL
    access_count = Column(Integer, default=0)  # Count of accesses

    def increment_access(self):
        self.access_count += 1
