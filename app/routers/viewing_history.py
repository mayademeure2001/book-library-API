from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from ..schemas.viewing_history import ViewingHistory, ViewingHistoryCreate, ViewingStatus
from ..dependencies import get_db, verify_api_key
from ..utils.pagination import pagination

router = APIRouter(
    prefix="/viewing-history",
    tags=["viewing history"]
)

@router.get("/", response_model=List[ViewingHistory])
async def get_all_history(
    pagination_params: tuple[int, int] = Depends(pagination),
    db=Depends(get_db),
    _: str = Depends(verify_api_key)
):
    try:
        skip, limit = pagination_params
        history_entries = list(db.viewing_history.values())
        return history_entries[skip : skip + limit]
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.post("/", response_model=ViewingHistory)
async def create_viewing_history(
    history: ViewingHistoryCreate, 
    db=Depends(get_db),
    _: str = Depends(verify_api_key)
):
    try:
        if history.movie_id not in db.movies:
            raise KeyError("Movie not found")
        
        new_history = ViewingHistory(
            id=len(db.viewing_history) + 1,
            **history.dict()
        )
        db.viewing_history[new_history.id] = new_history
        return new_history
    
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/movies/{movie_id}", response_model=List[ViewingHistory])
async def get_movie_history(
    movie_id: int,
    db=Depends(get_db),
    _: str = Depends(verify_api_key)
):
    try:
        if movie_id not in db.movies:
            raise KeyError("Movie not found")
        
        history_entries = [h for h in db.viewing_history.values() if h.movie_id == movie_id]
        return history_entries
    
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.delete("/{history_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_viewing_history(
    history_id: int, 
    db=Depends(get_db),
    _: str = Depends(verify_api_key)
):
    try:
        if history_id not in db.viewing_history:
            raise KeyError("Viewing history not found")
        del db.viewing_history[history_id]
    
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") 