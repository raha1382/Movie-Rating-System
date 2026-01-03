from pydantic import BaseModel, Field
from typing import Generic, TypeVar, List, Optional, Literal
from datetime import datetime

data_type = TypeVar("data_type")
data_type2 = TypeVar("data_type2")
data_type3 = TypeVar("data_type3")

class Response(BaseModel,  Generic[data_type]):
    status: Literal['success', 'failure'] = 'success'
    data: data_type

class MovieOut(BaseModel, Generic[data_type2]):
    id: int
    title: str = Field(..., min_length=1)
    release_year: int = Field(..., ge=1888, le=2026)
    director: data_type2
    genres: List[int]
    cast: Optional[str] = None
    average_rating: float | None = None
    ratings_count: int
    updated_at: datetime | None = None


class Moviein(BaseModel):
    title: str = Field(..., min_length=1)
    release_year: int = Field(..., ge=1888, le=2026)
    director_id: int
    genres: List[int]
    cast: Optional[str] = None

class Movieupdate(BaseModel):
    title: Optional[str] = None
    release_year: Optional[int] = Field(None, ge=1888, le=2026)
    director_id: Optional[int] = None
    genres: Optional[List[int]] = None
    cast: Optional[str] = None


class DirectorOut(BaseModel):
    id: int
    name: str


class MovieListItem(BaseModel, Generic[data_type3]):
    page: int
    page_size: int
    total_items: int
    items: data_type3


class MovieDetail(BaseModel):
    id: int
    title: str
    release_year: Optional[int]
    cast: Optional[str]
    director: str
    genres: List[str]
    average_rating: float
    ratings_count: int

