from sqlalchemy.orm import Session
from app.models import Rating
from app.repositories.movie import MovieRepository



class MovieService:

    @staticmethod
    def get_movies(db: Session, page: int = 1, page_size: int = 10):
        skip = (page - 1) * page_size
        raw_movies = MovieRepository.fetch_movies_with_aggregation(db, skip=skip, limit=page_size)

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

<<<<<<< Updated upstream
    @staticmethod
    def get_movie_detail(db: Session, movie_id: int):
        movie = MovieRepository.fetch_movie_by_id(db, movie_id)
        if not movie:
            return None

        avg_rating = db.query(func.coalesce(func.avg(Rating.score), 0))\
                       .filter(Rating.movie_id == movie.id).scalar()
        ratings_count = db.query(func.count(Rating.id))\
                          .filter(Rating.movie_id == movie.id).scalar()

        genres = [g.name for g in movie.genres]

        return {
            "id": movie.id,
            "title": movie.title,
            "release_year": movie.release_year,
            "cast": movie.cast,
            "director": movie.director.name if movie.director else None,
            "genres": genres,
            "average_rating": float(avg_rating),
            "ratings_count": ratings_count
        }

    @staticmethod
    def add_rating(db: Session, movie_id: int, score: int):
=======
    def add_rating(self, db: Session, movie_id: int, score: int):
>>>>>>> Stashed changes
        if not 1 <= score <= 10:
            raise ValueError("The score must be an integer between 1 and 10.")

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
  