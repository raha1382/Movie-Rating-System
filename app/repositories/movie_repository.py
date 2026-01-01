from sqlalchemy.orm import Session
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
