from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from ..schemas.authors import Author, AuthorCreate
from ..dependencies import get_db, verify_api_key, verify_admin_role
from ..utils.pagination import pagination

router = APIRouter(
    prefix="/authors",
    tags=["authors"]
)

@router.get("/", response_model=List[Author])
async def read_authors(
    pagination_params: tuple[int, int] = Depends(pagination),
    db=Depends(get_db),
    _: str = Depends(verify_api_key)
):
    try:
        skip, limit = pagination_params
        authors = list(db.authors.values())
        return authors[skip : skip + limit]
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.post("/", response_model=Author, status_code=status.HTTP_201_CREATED)
async def create_author(
    author: AuthorCreate, 
    db=Depends(get_db),
    _: str = Depends(verify_api_key),
    __: str = Depends(verify_admin_role)
):
    try:
        new_id = max(db.authors.keys() or (0,)) + 1
        new_author = Author(
            id=new_id,
            **author.dict()
        )
        db.authors[new_id] = new_author
        return new_author
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(
    author_id: int, 
    db=Depends(get_db),
    _: str = Depends(verify_api_key),
    __: str = Depends(verify_admin_role)
):
    try:
        if author_id not in db.authors:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
        
        # Check if author has any books
        author_books = [book for book in db.books.values() if book.author_id == author_id]
        if author_books:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete author with existing books"
            )
        
        db.authors.pop(author_id)
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") 