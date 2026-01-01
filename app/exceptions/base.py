from fastapi import status

class AppException(Exception):
    status_code: int = status.HTTP_400_BAD_REQUEST
    error_code: str = "APP_ERROR"

    def __init__(self, message: str):
        super().__init__(message)