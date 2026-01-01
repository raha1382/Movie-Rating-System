from sqlalchemy.orm import Session
from app.models.movie import Movie
from app.repositories.movie_repository import MovieRepository
from app.repositories.director_repository import DirectorRepository
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
    
    def select_movies(
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
