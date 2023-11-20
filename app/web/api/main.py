from fastapi import FastAPI

from app.web.api.routes import auth, todos, users

app = FastAPI()

for route in (auth, users, todos):
    app.include_router(route.router)
