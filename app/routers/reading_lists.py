from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from ..schemas.reading_lists import ReadingList, ReadingListCreate
from ..dependencies import get_db, verify_api_key
from ..utils.pagination import pagination

router = APIRouter(
    prefix="/reading-lists",
    tags=["reading lists"]
)

@router.get("/", response_model=List[ReadingList])
async def get_reading_lists(
    pagination_params: tuple[int, int] = Depends(pagination),
    db=Depends(get_db),
    _: str = Depends(verify_api_key)
):
    try:
        skip, limit = pagination_params
        reading_lists = list(db.reading_lists.values())
        return reading_lists[skip : skip + limit]
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.post("/", response_model=ReadingList)
async def create_reading_list(
    reading_list: ReadingListCreate, 
    db=Depends(get_db),
    _: str = Depends(verify_api_key)
):
    try:
        # Validate that all books exist
        for book_id in reading_list.book_ids:
            if book_id not in db.books:
                raise KeyError(f"Book with id {book_id} not found")
        
        new_list = ReadingList(
            id=len(db.reading_lists) + 1,
            **reading_list.dict()
        )
        db.reading_lists[new_list.id] = new_list
        return new_list
    
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.delete("/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reading_list(
    list_id: int, 
    db=Depends(get_db),
    _: str = Depends(verify_api_key)
):
    try:
        if list_id not in db.reading_lists:
            raise KeyError("Reading list not found")
        del db.reading_lists[list_id]
    
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") 