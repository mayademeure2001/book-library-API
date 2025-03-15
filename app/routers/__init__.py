from .authors import router as authors_router
from .books import router as books_router
from .reviews import router as reviews_router
from .reading_lists import router as reading_lists_router
from .reading_progress import router as reading_progress_router

__all__ = [
    "authors_router",
    "books_router",
    "reviews_router",
    "reading_lists_router",
    "reading_progress_router"
]
