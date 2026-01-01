from sqlalchemy.orm import Session, joinedload
from app.models.movie import Movie
from app.models.genre import Genre

class MovieRepository:

    def create(self, db: Session, movie: Movie) -> Movie:
        db.add(movie)
        db.commit()
        db.refresh(movie)
        return movie

    def get_genres_by_ids(self, db: Session, genre_ids: list[int]) -> list[Genre]:
        return db.query(Genre).filter(Genre.id.in_(genre_ids)).all()
    
    def get_by_id(self, db: Session, movie_id: int) -> Movie | None:
        return db.query(Movie).filter(Movie.id == movie_id).first()
    
    def save(self, db: Session, movie: Movie) -> Movie:
        db.add(movie)
        db.commit()
        db.refresh(movie)
        return movie
    
    def list_all(self, db: Session) -> list[Movie]:
        return db.query(Movie).all()
    
    def delete(self, db: Session, movie: Movie) -> None:
        db.delete(movie)
        db.commit()

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

