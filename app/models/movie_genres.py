from sqlalchemy import Column, Integer, String, ForeignKey, Table
from app.db.base import Base

movie_genres = Table(
    'movie_genres',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id', ondelete="CASCADE"), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id', ondelete="CASCADE"), primary_key=True)
)

