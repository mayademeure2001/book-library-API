from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from ..schemas.watchlists import WatchList, WatchListCreate
from ..dependencies import get_db, verify_api_key
from ..utils.pagination import pagination

router = APIRouter(
    prefix="/watchlists",
    tags=["watchlists"]
)

@router.get("/", response_model=List[WatchList])
async def get_watchlists(
    pagination_params: tuple[int, int] = Depends(pagination),
    db=Depends(get_db),
    _: str = Depends(verify_api_key)
):
    try:
        skip, limit = pagination_params
        watchlists = list(db.watchlists.values())
        return watchlists[skip : skip + limit]
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.post("/", response_model=WatchList)
async def create_watchlist(
    watchlist: WatchListCreate, 
    db=Depends(get_db),
    _: str = Depends(verify_api_key)
):
    try:
        # Validate that all movies exist
        for movie_id in watchlist.movie_ids:
            if movie_id not in db.movies:
                raise KeyError(f"Movie with id {movie_id} not found")
        
        new_list = WatchList(
            id=len(db.watchlists) + 1,
            **watchlist.dict()
        )
        db.watchlists[new_list.id] = new_list
        return new_list
    
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.delete("/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_watchlist(
    list_id: int, 
    db=Depends(get_db),
    _: str = Depends(verify_api_key)
):
    try:
        if list_id not in db.watchlists:
            raise KeyError("Watchlist not found")
        del db.watchlists[list_id]
    
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") 