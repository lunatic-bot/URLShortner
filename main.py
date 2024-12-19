from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import random
import string
from datetime import datetime
import models, schemas, database

# Create the FastAPI app
app = FastAPI()

# Mount the static files directory for CSS/JS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates for rendering HTML
templates = Jinja2Templates(directory="templates")

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create database tables (run this once)
@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=database.engine)

# Function to generate a random short URL
def generate_short_url(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Route to render the HTML page
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Route to shorten the URL
@app.post("/shorten/", response_model=schemas.URLResponse)
def shorten_url(request: schemas.URLRequest, db: Session = Depends(get_db)):
    # Check if the custom short URL already exists
    if request.custom_short_url:
        existing_url = db.query(models.URLMapping).filter(models.URLMapping.short_url == request.custom_short_url).first()
        if existing_url:
            raise HTTPException(status_code=400, detail="Custom short URL already exists.")
        short_url = request.custom_short_url
    else:
        short_url = generate_short_url()

    # Check if the original URL already exists
    existing_url = db.query(models.URLMapping).filter(models.URLMapping.original_url == request.original_url).first()
    if existing_url:
        return existing_url

    # Set expiration date if provided
    expiration_date = request.expiration_date if request.expiration_date else None

    # Store in the database
    new_url_mapping = models.URLMapping(
        original_url=request.original_url,
        short_url=short_url,
        expiration_date=expiration_date
    )
    db.add(new_url_mapping)
    db.commit()
    db.refresh(new_url_mapping)

    return new_url_mapping

# Route to redirect to the original URL
@app.get("/{short_url}", response_model=schemas.URLResponse)
def redirect_to_url(short_url: str, db: Session = Depends(get_db)):
    # Retrieve the original URL
    url_mapping = db.query(models.URLMapping).filter(models.URLMapping.short_url == short_url).first()

    if url_mapping is None:
        raise HTTPException(status_code=404, detail="Short URL not found")

    # Check if the URL has expired
    if url_mapping.expiration_date and url_mapping.expiration_date < datetime.utcnow():
        raise HTTPException(status_code=410, detail="Short URL has expired")

    # Increment the access count
    url_mapping.increment_access()
    db.commit()

    # Redirect to the original URL
    return {
        "original_url": url_mapping.original_url, 
        "short_url": url_mapping.short_url, 
        "access_count": url_mapping.access_count,
        "expiration_date": url_mapping.expiration_date
    }


# from fastapi import FastAPI, HTTPException, Depends
# from sqlalchemy.orm import Session
# import random
# import string
# from datetime import datetime
# import models, schemas, database

# # Create the FastAPI app
# app = FastAPI()

# # Dependency to get the database session
# def get_db():
#     db = database.SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # Create database tables (run this once)
# @app.on_event("startup")
# def on_startup():
#     models.Base.metadata.create_all(bind=database.engine)

# # Function to generate a random short URL
# def generate_short_url(length=6):
#     characters = string.ascii_letters + string.digits
#     return ''.join(random.choice(characters) for _ in range(length))

# # Route to shorten the URL
# @app.post("/shorten/", response_model=schemas.URLResponse)
# def shorten_url(request: schemas.URLRequest, db: Session = Depends(get_db)):
#     # Check if the custom short URL already exists
#     if request.custom_short_url:
#         existing_url = db.query(models.URLMapping).filter(models.URLMapping.short_url == request.custom_short_url).first()
#         if existing_url:
#             raise HTTPException(status_code=400, detail="Custom short URL already exists.")
#         short_url = request.custom_short_url
#     else:
#         short_url = generate_short_url()

#     # Check if the original URL already exists
#     existing_url = db.query(models.URLMapping).filter(models.URLMapping.original_url == request.original_url).first()
#     if existing_url:
#         return existing_url

#     # Set expiration date if provided
#     expiration_date = request.expiration_date if request.expiration_date else None

#     # Store in the database
#     new_url_mapping = models.URLMapping(
#         original_url=request.original_url,
#         short_url=short_url,
#         expiration_date=expiration_date
#     )
#     db.add(new_url_mapping)
#     db.commit()
#     db.refresh(new_url_mapping)

#     return new_url_mapping

# # Route to redirect to the original URL
# @app.get("/{short_url}", response_model=schemas.URLResponse)
# def redirect_to_url(short_url: str, db: Session = Depends(get_db)):
#     # Retrieve the original URL
#     url_mapping = db.query(models.URLMapping).filter(models.URLMapping.short_url == short_url).first()

#     if url_mapping is None:
#         raise HTTPException(status_code=404, detail="Short URL not found")

#     # Check if the URL has expired
#     if url_mapping.expiration_date and url_mapping.expiration_date < datetime.utcnow():
#         raise HTTPException(status_code=410, detail="Short URL has expired")

#     # Increment the access count
#     url_mapping.increment_access()
#     db.commit()

#     # Redirect to the original URL
#     return {
#             "original_url": url_mapping.original_url, 
#             "short_url": url_mapping.short_url, 
#             "access_count": url_mapping.access_count,
#             "expiration_date": url_mapping.expiration_date
#             }

