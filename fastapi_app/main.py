"""
Минимальное FastAPI приложение с Jinja2 шаблонами
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from .database import get_books, get_stats

app = FastAPI(title="Book Store", version="1.0")

# Шаблоны
templates_dir = Path(__file__).parent / "templates"
templates_dir.mkdir(exist_ok=True)
templates = Jinja2Templates(directory=str(templates_dir))

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    stats = get_stats()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "stats": stats
    })

@app.get("/books", response_class=HTMLResponse)
async def books(request: Request):
    books_data = get_books()
    return templates.TemplateResponse("books.html", {
        "request": request,
        "books": books_data
    })

@app.get("/api/books")
async def api_books():
    return {"books": get_books()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)