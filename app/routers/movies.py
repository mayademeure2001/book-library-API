from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from ..schemas.movies import Movie, MovieCreate
from ..dependencies import get_db, verify_api_key
from ..utils.pagination import pagination

router = APIRouter(
    prefix="/movies",
    tags=["movies"]
)

@router.get("/", response_model=List[Movie])
async def read_movies(
    genre: Optional[str] = None,
    director_id: Optional[int] = None,
    pagination_params: tuple[int, int] = Depends(pagination),
    db=Depends(get_db),
    _: str = Depends(verify_api_key)
):
    try:
        skip, limit = pagination_params
        movies = list(db.movies.values())
        
        if genre:
            movies = [movie for movie in movies if movie.genre.lower() == genre.lower()]
        if director_id:
            if director_id not in db.directors:
                raise KeyError("Director not found")
            movies = [movie for movie in movies if movie.director_id == director_id]
        
        return movies[skip : skip + limit]
    
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/{movie_id}", response_model=Movie)
async def read_movie(
    movie_id: int, 
    db=Depends(get_db),
    _: str = Depends(verify_api_key)
):
    try:
        if movie_id not in db.movies:
            raise KeyError("Movie not found")
        return db.movies[movie_id]
    
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.post("/", response_model=Movie)
async def create_movie(
    movie: MovieCreate, 
    db=Depends(get_db),
    _: str = Depends(verify_api_key)
):
    try:
        if movie.director_id not in db.directors:
            raise KeyError("Director not found")
        
        if not movie.imdb_id.startswith('tt'):
            raise ValueError("Invalid IMDB ID format")
        
        new_movie = Movie(
            id=len(db.movies) + 1,
            **movie.dict()
        )
        db.movies[new_movie.id] = new_movie
        return new_movie
    
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(
    movie_id: int, 
    db=Depends(get_db),
    _: str = Depends(verify_api_key)
):
    try:
        if movie_id not in db.movies:
            raise KeyError("Movie not found")
        
        # Delete associated reviews
        db.reviews = {
            k: v for k, v in db.reviews.items()
            if v.movie_id != movie_id
        }
        
        # Remove from watchlists
        for watchlist in db.watchlists.values():
            if movie_id in watchlist.movie_ids:
                watchlist.movie_ids.remove(movie_id)
        
        # Delete viewing history
        db.viewing_history = {
            k: v for k, v in db.viewing_history.items()
            if v.movie_id != movie_id
        }
        
        del db.movies[movie_id]
        return {"message": "Movie and related items deleted"}
    
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") 