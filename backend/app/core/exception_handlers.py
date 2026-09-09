import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import AppException


logger = logging.getLogger(__name__)

ALLOWED_ORIGINS = {
    "http://localhost:5173",
    "http://127.0.0.1:5173",
}


def _with_cors(request: Request, response: JSONResponse) -> JSONResponse:
    """
    FastAPI attaches bare Exception handlers to ServerErrorMiddleware,
    which runs outside CORSMiddleware. Re-apply CORS on those responses
    so the browser can read the error body.
    """

    origin = request.headers.get("origin")

    if origin in ALLOWED_ORIGINS:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Vary"] = "Origin"

    return response


async def app_exception_handler(
    request: Request,
    exc: AppException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
            }
        },
    )


async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    logger.exception(
        "Unhandled exception: %s %s",
        request.method,
        request.url.path,
    )

    return _with_cors(
        request,
        JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred.",
                }
            },
        ),
    )
