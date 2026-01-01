from pydantic import BaseModel, Field
from typing import List, Optional

class DirectorOut(BaseModel):
    id: int
    name: str


class MovieListItem(BaseModel):
    id: int
    title: str
    release_year: Optional[int]
    cast: Optional[str]
    director: str
    genres: List[str]
    average_rating: float
    ratings_count: int


class MovieDetail(BaseModel):
    id: int
    title: str
    release_year: Optional[int]
    cast: Optional[str]
    director: str
    genres: List[str]
    average_rating: float
    ratings_count: int
