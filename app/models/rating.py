from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from app.db.base import Base

class Rating(Base):
    __tablename__ = "movie_ratings"
    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"))
    score = Column(Integer, nullable=False) 
    
    movie = relationship("Movie", back_populates="ratings")