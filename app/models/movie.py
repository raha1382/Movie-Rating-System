from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.movie_genres import movie_genres

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    director_id = Column(Integer, ForeignKey("directors.id"))
    release_year = Column(Integer)
    cast = Column(Text)

    director = relationship("Director", back_populates="movies")
    genres = relationship("Genre", secondary=movie_genres, back_populates="movies")
    ratings = relationship("Rating", back_populates="movie", cascade="all, delete-orphan")
