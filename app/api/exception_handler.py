from fastapi.exceptions import RequestValidationError
from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions.base import AppException


# for pydantic errors
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    first_error = exc.errors()[0]
    loc = first_error.get("loc", [])
    msg = first_error.get("msg", "Invalid input")
    
    return JSONResponse(
        status_code=422,
        content={
            "status": "failure",
            "error": {
                "code": "VALIDATION_ERROR",
                "status": 422,
                "message": msg
            }
        }
    )

#for service errors
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "failure",
            "error": {
                "code": exc.error_code,
                "status": exc.status_code,
                "message": str(exc)
            }
        }
    )
