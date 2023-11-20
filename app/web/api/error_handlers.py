from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.web.api.main import app
from app.web.errors import WebError


@app.exception_handler(WebError)
async def web_error_handler(request: Request, error: WebError):
    return JSONResponse(
        status_code=error.status_code,
        content=jsonable_encoder({"detail": error.detail}),
    )
