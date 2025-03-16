from .directors import router as directors_router
from .movies import router as movies_router
from .reviews import router as reviews_router
from .watchlists import router as watchlists_router
from .viewing_history import router as viewing_history_router

__all__ = [
    "directors_router",
    "movies_router",
    "reviews_router",
    "watchlists_router",
    "viewing_history_router"
]
