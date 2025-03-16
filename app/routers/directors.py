from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from ..schemas.directors import Director, DirectorCreate
from ..dependencies import get_db, verify_api_key, verify_admin_role
from ..utils.pagination import pagination

router = APIRouter(
    prefix="/directors",
    tags=["directors"]
)

@router.get("/", response_model=List[Director])
async def read_directors(
    pagination_params: tuple[int, int] = Depends(pagination),
    db=Depends(get_db),
    _: str = Depends(verify_api_key)
):
    try:
        skip, limit = pagination_params
        directors = list(db.directors.values())
        return directors[skip : skip + limit]
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.post("/", response_model=Director, status_code=status.HTTP_201_CREATED)
async def create_director(
    director: DirectorCreate, 
    db=Depends(get_db),
    _: str = Depends(verify_api_key),
    __: str = Depends(verify_admin_role)
):
    try:
        new_id = max(db.directors.keys() or (0,)) + 1
        new_director = Director(
            id=new_id,
            **director.dict()
        )
        db.directors[new_id] = new_director
        return new_director
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.delete("/{director_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_director(
    director_id: int, 
    db=Depends(get_db),
    _: str = Depends(verify_api_key),
    __: str = Depends(verify_admin_role)
):
    try:
        if director_id not in db.directors:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Director not found")
        
        # Check if director has any movies
        director_movies = [movie for movie in db.movies.values() if movie.director_id == director_id]
        if director_movies:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete director with existing movies"
            )
        
        db.directors.pop(director_id)
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") 