from .schemas.directors import Director
from .schemas.movies import Movie
from .schemas.reviews import Review
from .schemas.watchlists import WatchList
from .schemas.viewing_history import ViewingHistory

class DummyDatabase:
    directors: dict[int, Director] = {}
    movies: dict[int, Movie] = {}
    reviews: dict[int, Review] = {}
    watchlists: dict[int, WatchList] = {}
    viewing_history: dict[int, ViewingHistory] = {}


db = DummyDatabase() 