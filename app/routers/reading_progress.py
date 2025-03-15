from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from ..schemas.reading_progress import ReadingProgress, ReadingProgressCreate, ReadingStatus
from ..dependencies import get_db, verify_api_key
from ..utils.pagination import pagination

router = APIRouter(
    prefix="/reading-progress",
    tags=["reading progress"]
)

@router.get("/", response_model=List[ReadingProgress])
async def get_all_progress(
    pagination_params: tuple[int, int] = Depends(pagination),
    db=Depends(get_db),
    _: str = Depends(verify_api_key)
):
    try:
        skip, limit = pagination_params
        progress_entries = list(db.reading_progress.values())
        return progress_entries[skip : skip + limit]
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.post("/", response_model=ReadingProgress)
async def create_reading_progress(
    progress: ReadingProgressCreate, 
    db=Depends(get_db),
    _: str = Depends(verify_api_key)
):
    try:
        if progress.book_id not in db.books:
            raise KeyError("Book not found")
        
        new_progress = ReadingProgress(
            id=len(db.reading_progress) + 1,
            **progress.dict()
        )
        db.reading_progress[new_progress.id] = new_progress
        return new_progress
    
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/books/{book_id}", response_model=List[ReadingProgress])
async def get_book_progress(
    book_id: int,
    db=Depends(get_db),
    _: str = Depends(verify_api_key)
):
    try:
        if book_id not in db.books:
            raise KeyError("Book not found")
        
        progress_entries = [p for p in db.reading_progress.values() if p.book_id == book_id]
        return progress_entries
    
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.delete("/{progress_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reading_progress(
    progress_id: int, 
    db=Depends(get_db),
    _: str = Depends(verify_api_key)
):
    try:
        if progress_id not in db.reading_progress:
            raise KeyError("Reading progress not found")
        del db.reading_progress[progress_id]
    
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") 