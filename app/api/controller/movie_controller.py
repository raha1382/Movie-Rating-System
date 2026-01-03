from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List

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

from app.exceptions.movie_exceptions import MovieNotFoundError

from app.logging_config import setup_logging
logger = setup_logging()

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

@router.get("/", response_model=Response[MovieListItem[list[MovieDetail]]], status_code=status.HTTP_200_OK)
def list_movies(
    title: str | None = Query(None, description="Filter by movie title"),
    director: str | None = Query(None, description="Filter by director name"),
    genre: str | None = Query(None, description="Filter by genre"),
    release_year: int | None = Query(None, description="Filter by movie release year"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    route = "/api/v1/movies"
    logger.info(f"Listing movies: route={route}, title={title}, director={director}, genre={genre}, year={release_year}, page={page}, page_size={page_size}")


    result = movie_service.get_movies(
        db=db,
        title=title,
        director=director,
        genre=genre,
        release_year=release_year,
        page=page,
        page_size=page_size
    )
    
    logger.info(f"Movies listed successfully (count={len(result['data'])})")

    result_items = [
        MovieDetail(
            id=m["id"],
            title=m["title"],
            release_year=m["release_year"],
            cast=m["cast"],
            director=m["director"],
            genres=m["genres"],
            average_rating=m["average_rating"],
            ratings_count=m["ratings_count"],
        )
        for m in result["data"]
    ]

    return Response(
        status="success",
        data=MovieListItem(
            page= result["page"],
            page_size= result["page_size"],
            total_items= result["total_items"],
            items= result_items
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
            release_year = data["release_year"],
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
    route = f"/api/v1/movies/{movie_id}/ratings"
    logger.info(f"Rating movie (movie_id={movie_id}, rating={payload.score}, route={route})")

    rating = movie_service.add_rating(
        db=db,
        movie_id=movie_id,
        score=payload.score
    )

    logger.info(f"Rating saved successfully (movie_id={movie_id}, rating={payload.score})")

    return Response(
        status = "success",
        data = RatingOut( 
            rating_id = rating.id,
            movie_id = rating.movie_id,
            score = rating.score
        )

    )