from .schemas.authors import Author
from .schemas.books import Book
from .schemas.reviews import Review
from .schemas.reading_lists import ReadingList
from .schemas.reading_progress import ReadingProgress

class DummyDatabase:
    authors: dict[int, Author] = {}
    books: dict[int, Book] = {}
    reviews: dict[int, Review] = {}
    reading_lists: dict[int, ReadingList] = {}
    reading_progress: dict[int, ReadingProgress] = {}


db = DummyDatabase() 