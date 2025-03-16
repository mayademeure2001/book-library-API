from fastapi import FastAPI
from .routers import directors_router, movies_router, reviews_router, watchlists_router, viewing_history_router
from .schemas import Movie, Director, Review, WatchList

app = FastAPI(title="Movie Database API")

app.include_router(directors_router)
app.include_router(movies_router)
app.include_router(reviews_router)
app.include_router(watchlists_router)
app.include_router(viewing_history_router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Movie Database API",
        "docs": "/docs",
        "endpoints": {
            "directors": "/directors",
            "movies": "/movies",
            "reviews": "/reviews",
            "watchlists": "/watchlists",
            "viewing_history": "/viewing-history"
        }
    } 