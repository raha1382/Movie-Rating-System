from sqlalchemy.orm import Session
from app.models.movie import Movie
from app.repositories.movie_repository import MovieRepository
from app.repositories.director_repository import DirectorRepository
from app.models.rating import Rating
from sqlalchemy import func
from app.exceptions.movie_exceptions import (
    MovieNotFoundError,
    InvalidTitleError,
    InvalidReleaseYearError,
    DirectorNotFoundError,
    InvalidGenreError,
    InvalidRatingError
)



class MovieService:

    def __init__(self):
        self.movie_repo = MovieRepository()
        self.director_repo = DirectorRepository()

    # CRUD Methods

    def create_movie(
        self,
        db: Session,
        title: str,
        release_year: int,
        director_id: int,
        genre_ids: list[int],
        cast: str | None = None
    ) -> Movie:

        if not title or not title.strip():
            raise InvalidTitleError()

        if release_year and (release_year < 1888 or release_year > 2100):
            raise InvalidReleaseYearError()

        director = self.director_repo.get_by_id(db, director_id)
        if not director:
            raise DirectorNotFoundError()

        genres = self.movie_repo.get_genres_by_ids(db, genre_ids)
        if len(genres) != len(genre_ids):
            raise InvalidGenreError()

        movie = Movie(
            title=title,
            release_year=release_year,
            director_id=director_id,
            cast=cast,
            genres=genres
        )

        return self.movie_repo.create(db, movie)
    
    def update_movie(
        self,
        db: Session,
        movie_id: int,
        *,
        title: str | None = None,
        release_year: int | None = None,
        director_id: int | None = None,
        cast: str | None = None,
        genre_ids: list[int] | None = None
    ):
        movie = self.movie_repo.get_by_id(db, movie_id)
        if not movie:
            raise MovieNotFoundError(movie_id)

        if title is not None and not title.strip():
            raise InvalidTitleError()

        if release_year is not None and (release_year < 1888 or release_year > 2100):
            raise InvalidReleaseYearError(release_year)

        if director_id is not None:
            director = self.director_repo.get_by_id(db, director_id)
            if not director:
                raise DirectorNotFoundError(director_id)
            movie.director_id = director_id

        if title is not None:
            movie.title = title

        if release_year is not None:
            movie.release_year = release_year

        if cast is not None:
            movie.cast = cast

        if genre_ids is not None:
            genres = self.movie_repo.get_genres_by_ids(db, genre_ids)
            if len(genres) != len(genre_ids):
                raise InvalidGenreError(genre_ids)

            movie.genres.clear()
            movie.genres.extend(genres)

        return self.movie_repo.save(db, movie)
    
    def list_movies(
        self,
        db: Session,
        title: str | None = None,
        release_year: int | None = None,
        genre_name: str | None = None,
        page: int = 1,
        page_size: int = 10
    ) -> dict:

        movies = self.movie_repo.list_all(db) 

        if title:
            movies = [m for m in movies if title.lower() in m.title.lower()]

        if release_year:
            movies = [m for m in movies if m.release_year == release_year]

        if genre_name:
            movies = [
                m for m in movies
                if any(g.name.lower() == genre_name.lower() for g in m.genres)
            ]

        total = len(movies)
        start = (page - 1) * page_size
        end = start + page_size
        paginated = movies[start:end]

        return {
            "items": paginated,
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": (total + page_size - 1) // page_size
        }
    
    def delete_movie(self, db: Session, movie_id: int) -> None:
        movie = self.movie_repo.get_by_id(db, movie_id)
        if not movie:
            raise MovieNotFoundError(movie_id)

        self.movie_repo.delete(db, movie)

    # Aggregation / Ratings Methods

    def get_movies(self, db: Session, page: int = 1, page_size: int = 10):
        skip = (page - 1) * page_size
        raw_movies = self.movie_repo.fetch_movies_with_aggregation(db, skip=skip, limit=page_size)

        result = []
        for movie, director_name, avg_rating, ratings_count in raw_movies:
            genres = [g.name for g in movie.genres]
            result.append({
                "id": movie.id,
                "title": movie.title,
                "release_year": movie.release_year,
                "cast": movie.cast,
                "director": director_name,
                "genres": genres,
                "average_rating": float(avg_rating),
                "ratings_count": ratings_count
            })

        return {
            "page": page,
            "page_size": page_size,
            "data": result
        }

    def add_rating(self, db: Session, movie_id: int, score: int):

        if not 1 <= score <= 10:
            raise InvalidRatingError(score)

        rating = Rating(movie_id=movie_id, score=score)
        db.add(rating)
        db.commit()
        db.refresh(rating)
        return rating

    def get_movie_detail(self, db: Session, movie_id: int):
        row = self.movie_repo.fetch_movie_with_aggregation(db, movie_id)
        if not row:
            return None

        movie, director_name, avg_rating, ratings_count = row
        genres = [g.name for g in movie.genres]

        return {
            "id": movie.id,
            "title": movie.title,
            "release_year": movie.release_year,
            "cast": movie.cast,
            "director": director_name,
            "genres": genres,
            "average_rating": float(avg_rating),
            "ratings_count": ratings_count
            }
  