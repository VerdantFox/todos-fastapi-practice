from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Cookie, Response

from app.datastore.database import DBDependency
from app.web import auth, errors, web_models
from app.web import field_types as ft

# ----------- Routers -----------
router = APIRouter(tags=["auth"], prefix="/auth")


@router.post("/token")
async def login_for_access_token(
    db: DBDependency,
    username: ft.StrFormField,
    password: ft.StrFormField,
):
    user = auth.authenticate_user(username=username, password=password, db=db)
    return auth.create_access_token(user=user)
