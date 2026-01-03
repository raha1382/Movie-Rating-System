from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from datetime import datetime
from app.db.session import get_db
from app.services.movie_service import MovieService
from app.api.schemas.movie import (
    Moviein,
    Movieupdate,
    MovieListItem,
    MovieDetail,
    Response,
    DirectorOut,
    MovieOut
)
from app.api.schemas.rating import RatingOut
from app.api.schemas.rating import RatingCreate
from app.api.schemas.rating import RatingCreate

from app.exceptions.movie_exceptions import MovieNotFoundError

router = APIRouter(prefix="/api/v1/movies", tags=["Movies"])
movie_service = MovieService()


@router.post("/", response_model=Response[MovieOut[DirectorOut]], status_code=status.HTTP_201_CREATED)
def create_movie(
    payload: Moviein,
    db: Session = Depends(get_db)
):
    movie = movie_service.create_movie(
        db=db,
        title=payload.title,
        release_year=payload.release_year,
        director_id=payload.director_id,
        genre_ids=payload.genres,
        cast=payload.cast
    )

    return Response(
        status = "success",
        data = MovieOut(
            id= movie.id,
            title= movie.title,
            release_year= movie.release_year,
            director = DirectorOut(
                id= movie.director.id,
                name= movie.director.name
            ),
            genres= [genre.id for genre in movie.genres],
            cast= movie.cast,
            average_rating= None,
            ratings_count= 0,
            updated_at = None
        )
    )

@router.put("/{movie_id}", response_model=Response[MovieOut[DirectorOut]], status_code=status.HTTP_200_OK)
def update_movie(
    movie_id: int,
    payload: Movieupdate,
    db: Session = Depends(get_db)
):
    movie = movie_service.update_movie(
        db=db,
        movie_id=movie_id,
        title=payload.title,
        release_year=payload.release_year,
        director_id=payload.director_id,
        cast=payload.cast,
        genre_ids=payload.genres
    )
    movie_result = movie_service.get_movie_detail(db=db,movie_id=movie.id)
    
    return Response(
        status = "success",
        data = MovieOut(
            id= movie.id,
            title= movie.title,
            release_year= movie.release_year,
            director = DirectorOut(
                id= movie.director.id,
                name= movie.director.name
            ),
            genres= [genre.id for genre in movie.genres],
            cast= movie.cast,
            average_rating= movie_result["average_rating"],
            ratings_count= movie_result["ratings_count"],
            updated_at = datetime.utcnow().isoformat() + "Z"
        )
    )


@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(
    movie_id: int,
    db: Session = Depends(get_db)
):
    movie_service.delete_movie(db, movie_id)
    return None

@router.get("/", response_model=Response[MovieListItem], status_code=status.HTTP_200_OK)
def list_movies(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    data = movie_service.get_movies(db, page, page_size)
    return Response(
        status = "success",
        data = MovieListItem(
            id = data["id"],
            title = data["title"],
            release_year = data["Orelease_year"],
            cast = data["cast"],
            director = data["director"],
            genres = data["genres"],
            average_rating = data["average_rating"],
            ratings_count = data["ratings_count"]
        )      
    )

@router.get("/{movie_id}", response_model=Response[MovieDetail], status_code=status.HTTP_200_OK)
def get_movie_detail(
    movie_id: int,
    db: Session = Depends(get_db)
):
    data = movie_service.get_movie_detail(db, movie_id)
    if not data:
        raise MovieNotFoundError(movie_id)

    return Response(
        status = "success",
        data = MovieDetail(
            id = data["id"],
            title = data["title"],
            release_year = data["Orelease_year"],
            cast = data["cast"],
            director = data["director"],
            genres = data["genres"],
            average_rating = data["average_rating"],
            ratings_count = data["ratings_count"]
        )      
    )
       
@router.post("/{movie_id}/ratings", response_model=Response[RatingOut], status_code=status.HTTP_201_CREATED)
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

    return Response(
        status = "success",
        data = RatingOut( 
            rating_id = rating.id,
            movie_id = rating.movie_id,
            score = rating.score
        )

    )