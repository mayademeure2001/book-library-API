from fastapi import FastAPI
from .routers import authors_router, books_router, reviews_router, reading_lists_router, reading_progress_router
from .schemas import Book, Author, Review, ReadingList

app = FastAPI(title="Book Library Management System")

app.include_router(authors_router)
app.include_router(books_router)
app.include_router(reviews_router)
app.include_router(reading_lists_router)
app.include_router(reading_progress_router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Book Library Management System",
        "docs": "/docs",
        "endpoints": {
            "authors": "/authors",
            "books": "/books",
            "reviews": "/reviews",
            "reading_lists": "/reading-lists",
            "reading_progress": "/reading-progress"
        }
    } 