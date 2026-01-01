from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.movie_service import MovieService
from app.schemas.movie import (
    MovieCreate,
    MovieUpdate,
)
from app.schemas.rating import RatingCreate
from app.exceptions.movie_exceptions import MovieNotFoundError

router = APIRouter(prefix="/api/v1/movies", tags=["Movies"])
movie_service = MovieService()

# ----------------------------
# List movies (aggregation)
# ----------------------------
@router.get("/", status_code=status.HTTP_200_OK)
def list_movies(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    data = movie_service.get_movies(db, page, page_size)
    return {
        "status": "success",
        "data": data
    }

# ----------------------------
# Movie detail
# ----------------------------
@router.get("/{movie_id}", status_code=status.HTTP_200_OK)
def get_movie_detail(
    movie_id: int,
    db: Session = Depends(get_db)
):
    movie = movie_service.get_movie_detail(db, movie_id)
    if not movie:
        raise MovieNotFoundError(movie_id)

    return {
        "status": "success",
        "data": movie
    }
       
# ----------------------------
# Add rating
# ----------------------------
@router.post("/{movie_id}/ratings", status_code=status.HTTP_201_CREATED)
def add_rating(
    movie_id: int,
    payload: RatingCreate,
    db: Session = Depends(get_db)
):
    rating = movie_service.add_rating(
        db=db,
        movie_id=movie_id,
        score=payload.score
    )

    return {
        "status": "success",
        "data": {
            "rating_id": rating.id,
            "movie_id": rating.movie_id,
            "score": rating.score
        }
    }
