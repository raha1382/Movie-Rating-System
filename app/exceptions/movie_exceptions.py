from fastapi import status
from app.exceptions.base import AppException


class MovieError(AppException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    error_code = "MOVIE_VALIDATION_ERROR"


class InvalidTitleError(MovieError):
    def __init__(self):
        super().__init__("title is required")


class InvalidReleaseYearError(MovieError):
    def __init__(self):
        super().__init__("release_year is invalid")


class DirectorNotFoundError(MovieError):
    def __init__(self, director_id: int):
        super().__init__(f"director with id {director_id} not found")
        self.director_id = director_id


class InvalidGenreError(MovieError):
    def __init__(self):
        super().__init__("one or more genre ids are invalid")

class MovieNotFoundError(MovieError):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = "MOVIE_NOT_FOUND"

    def __init__(self, movie_id: int):
        super().__init__(f"movie with id {movie_id} not found")
        self.movie_id = movie_id


class InvalidRatingError(ValueError):
    def __init__(self, score):
        super().__init__(f"The score must be an integer between 1 and 10. Got: {score}")
        self.score = score


