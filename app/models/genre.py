from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from app.db.base import Base
from movie_genres import movie_genres

class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    
    movies = relationship("Movie", secondary=movie_genres, back_populates="genres")