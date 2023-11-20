from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Cookie, Request, Response
from fastapi.responses import HTMLResponse

from app.datastore.database import DBDependency
from app.web import auth, errors, web_models
from app.web import field_types as ft
from app.web.auth import OptionalCookieDependency
from app.web.html.const import templates

# ----------- Routers -----------
router = APIRouter(tags=["auth"], prefix="/auth")
ACCESS_TOKEN = "access_token"


@router.post("/token")
async def login_for_access_token(
    response: Response,
    db: DBDependency,
    username: ft.StrFormField,
    password: ft.StrFormField,
):
    user = auth.authenticate_user(username=username, password=password, db=db)
    token = auth.create_access_token(user=user)
    response.set_cookie(
        key=ACCESS_TOKEN, value=token.access_token, httponly=True, secure=True
    )
    return token


REFRESH_ACCESS_PARTIAL = "shared/partials/refresh_access.html"


@router.get("/refresh-token-cookie")
async def refresh_access_token(
    request: Request,
    access_token: OptionalCookieDependency = None,
    remaining_time: int | None = None,
):
    """Refresh the access token, if one is already set."""
    if not access_token:
        return templates.TemplateResponse(
            REFRESH_ACCESS_PARTIAL,
            {"request": request, "no_content": True},
        )

    try:
        token = await auth.refresh_token(
            access_token=access_token, remaining_time=remaining_time
        )
    except errors.UserNotValidatedError:
        response = templates.TemplateResponse(
            REFRESH_ACCESS_PARTIAL, {"request": request, "no_content": True}
        )
        response.delete_cookie(key=ACCESS_TOKEN)
        return response
    response = templates.TemplateResponse(REFRESH_ACCESS_PARTIAL, {"request": request})
    response.set_cookie(key=ACCESS_TOKEN, value=token.access_token)
    return response
