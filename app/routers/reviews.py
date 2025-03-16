from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from ..schemas.reviews import Review, ReviewCreate
from ..dependencies import get_db, verify_api_key
from ..utils.pagination import pagination

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"]
)

@router.get("/", response_model=List[Review])
async def read_reviews(
    pagination_params: tuple[int, int] = Depends(pagination),
    db=Depends(get_db),
    _: str = Depends(verify_api_key)
):
    try:
        skip, limit = pagination_params
        reviews = list(db.reviews.values())
        return reviews[skip : skip + limit]
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/{review_id}", response_model=Review)
async def read_review(
    review_id: int, 
    db=Depends(get_db),
    _: str = Depends(verify_api_key)
):
    try:
        if review_id not in db.reviews:
            raise KeyError("Review not found")
        return db.reviews[review_id]
    
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.post("/", response_model=Review)
async def create_review(
    review: ReviewCreate, 
    db=Depends(get_db),
    _: str = Depends(verify_api_key)
):
    try:
        if review.movie_id not in db.movies:
            raise KeyError("Movie not found")
        
        # Validate rating
        if isinstance(review.rating, int) and not (1 <= review.rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        
        new_review = Review(
            id=len(db.reviews) + 1,
            **review.dict()
        )
        db.reviews[new_review.id] = new_review
        return new_review
    
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    review_id: int, 
    db=Depends(get_db),
    _: str = Depends(verify_api_key)
):
    try:
        if review_id not in db.reviews:
            raise KeyError("Review not found")
        del db.reviews[review_id]
    
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") 