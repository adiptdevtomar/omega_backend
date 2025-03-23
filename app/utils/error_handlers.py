from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.utils.response_formatter import format_response

async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=format_response(message=exc.detail, success=False),
    )

async def general_exception_handler(request: Request, exc: Exception):
    # Wrap all exceptions as CustomException
    custom_exc = CustomException(
        name="UnhandledException",
        detail=str(exc),
        status_code=500
    )
    return await custom_exception_handler(request, custom_exc)

class CustomException(Exception):
    def __init__(self, name: str, detail: str, status_code: int = 400):
        self.name = name
        self.detail = detail
        self.status_code = status_code

async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content=format_response(message=exc.detail, success=False, data={"error": exc.name}),
    )