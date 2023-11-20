from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.web.html import flash_messages
from app.web.html.const import STATIC_DIR, templates
from app.web.html.error_handlers import register_error_handlers
from app.web.html.routes import auth, errors, todos, users

SESSION_SECRET = "SUPER-SECRET-KEY"

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)

routes = [auth, errors, todos, users]
for route in routes:
    app.include_router(route.router)

register_error_handlers(app)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates.env.globals["get_flashed_messages"] = flash_messages.get_flashed_messages


@app.get("/")
async def home(request: Request):
    return RedirectResponse(
        url=request.url_for("html:get_todos"), status_code=status.HTTP_302_FOUND
    )
