from pydantic import BaseModel, Field


class RatingCreate(BaseModel):
    score: int = Field(..., ge=1, le=10)


class RatingOut(BaseModel):
    rating_id: int
    movie_id: int
    score: int
    
