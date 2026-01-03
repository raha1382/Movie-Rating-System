from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base

class Rating(Base):
    __tablename__ = "movie_ratings"
    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"))
    score = Column(Integer, nullable=False, default=0)
    rated_at = Column(DateTime(timezone=False), nullable=True)

    
    movie = relationship("Movie", back_populates="ratings")