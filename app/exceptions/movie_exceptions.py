class MovieError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


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
    error_code = "MOVIE_NOT_FOUND"

    def __init__(self, movie_id: int):
        super().__init__(f"movie with id {movie_id} not found")
        self.movie_id = movie_id
