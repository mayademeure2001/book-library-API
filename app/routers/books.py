from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from ..schemas.books import Book, BookCreate
from ..dependencies import get_db, verify_api_key
from ..utils.pagination import pagination

router = APIRouter(
    prefix="/books",
    tags=["books"]
)

@router.get("/", response_model=List[Book])
async def read_books(
    genre: Optional[str] = None,
    author_id: Optional[int] = None,
    pagination_params: tuple[int, int] = Depends(pagination),
    db=Depends(get_db),
    _: str = Depends(verify_api_key)
):
    try:
        skip, limit = pagination_params
        books = list(db.books.values())
        
        if genre:
            books = [book for book in books if book.genre.lower() == genre.lower()]
        if author_id:
            if author_id not in db.authors:
                raise KeyError("Author not found")
            books = [book for book in books if book.author_id == author_id]
        
        return books[skip : skip + limit]
    
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/{book_id}", response_model=Book)
async def read_book(
    book_id: int, 
    db=Depends(get_db),
    _: str = Depends(verify_api_key)
):
    try:
        if book_id not in db.books:
            raise KeyError("Book not found")
        return db.books[book_id]
    
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.post("/", response_model=Book)
async def create_book(
    book: BookCreate, 
    db=Depends(get_db),
    _: str = Depends(verify_api_key)
):
    try:
        if book.author_id not in db.authors:
            raise KeyError("Author not found")
        
        if not (10 <= len(book.isbn) <= 13):
            raise ValueError("Invalid ISBN length")
        
        new_book = Book(
            id=len(db.books) + 1,
            **book.dict()
        )
        db.books[new_book.id] = new_book
        return new_book
    
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: int, 
    db=Depends(get_db),
    _: str = Depends(verify_api_key)
):
    try:
        if book_id not in db.books:
            raise KeyError("Book not found")
        
        # Delete associated reviews
        db.reviews = {
            k: v for k, v in db.reviews.items()
            if v.book_id != book_id
        }
        
        # Remove from reading lists
        for reading_list in db.reading_lists.values():
            if book_id in reading_list.book_ids:
                reading_list.book_ids.remove(book_id)
        
        # Delete reading progress
        db.reading_progress = {
            k: v for k, v in db.reading_progress.items()
            if v.book_id != book_id
        }
        
        del db.books[book_id]
        return {"message": "Book and related items deleted"}
    
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") 