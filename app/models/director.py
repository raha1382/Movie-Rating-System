from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from app.db.base import Base

class Director(Base):
    __tablename__ = "directors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    birth_year = Column(Integer)
    description = Column(Text)
    
    movies = relationship("Movie", back_populates="director")