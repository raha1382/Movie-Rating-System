from pydantic import BaseModel, Field
from typing import List, Optional



class MovieCreate(BaseModel):
    title: str = Field(..., min_length=1)
    release_year: int = Field(..., ge=1888, le=2026)
    director_id: int
    genres: List[int]
    cast: Optional[str] = None


class MovieUpdate(BaseModel):
    title: Optional[str] = None
    release_year: Optional[int] = Field(None, ge=1888, le=2100)
    director_id: Optional[int] = None
    genres: Optional[List[int]] = None
    cast: Optional[str] = None


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

