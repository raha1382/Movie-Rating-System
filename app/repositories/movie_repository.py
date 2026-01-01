from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from app.models import Movie, Rating, Director, Genre

class MovieRepository:

    @staticmethod
    def fetch_movies_with_aggregation(db: Session, skip: int = 0, limit: int = 10):
       
        query = (
            db.query(
                Movie,
                Director.name.label("director_name"),
                func.coalesce(func.avg(Rating.score), 0).label("average_rating"),
                func.count(Rating.id).label("ratings_count")
            )
            .join(Movie.director)
            .outerjoin(Movie.ratings)
            .group_by(Movie.id, Director.name)
            .order_by(Movie.id)
            .offset(skip)
            .limit(limit)
        )
        return query.all()

    @staticmethod
    def fetch_movie_by_id(db: Session, movie_id: int):
        
        movie = db.query(Movie).options(joinedload(Movie.genres), joinedload(Movie.director))\
                  .filter(Movie.id == movie_id).first()
        return movie
