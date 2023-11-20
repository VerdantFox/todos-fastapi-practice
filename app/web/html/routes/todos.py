from typing import Annotated, cast

from fastapi import APIRouter, Path, Request, status
from fastapi.responses import HTMLResponse
from wtforms import (
    BooleanField,
    Form,
    StringField,
    validators,
)

from app.datastore import db_models
from app.datastore.database import DBDependency
from app.services import todos
from app.web import errors
from app.web.api import api_models
from app.web.auth import LoggedInUser
from app.web.html.const import templates

# ----------- Routers -----------
router = APIRouter(tags=["todos"], prefix="/todos")

TODO_PARTIAL_TEMPLATE = "todos/partials/todo.html"


@router.get("", response_class=HTMLResponse)
async def get_todos(request: Request, db: DBDependency, current_user: LoggedInUser):
    todos_list_db = await todos.get_todos_list(db, current_user)

    todos_list_api = [
        api_models.TodoOutLimited(**todo.__dict__) for todo in todos_list_db
    ]

    return templates.TemplateResponse(
        "todos/todos.html",
        {"request": request, "current_user": current_user, "todos": todos_list_api},
    )


class CreateTodoForm(Form):
    title: StringField = StringField(
        "Title", validators=[validators.Length(min=3, max=25)]
    )


@router.post("")
async def add_todo(request: Request, db: DBDependency, current_user: LoggedInUser):
    form_data = await request.form()
    create_todo_form = CreateTodoForm(**form_data)
    if not create_todo_form.validate():
        return HTMLResponse(content="", status_code=status.HTTP_400_BAD_REQUEST)
    todo = await todos.add_todo(
        db=db, current_user=current_user, title=create_todo_form.title.data
    )
    db.refresh(todo)

    return templates.TemplateResponse(
        TODO_PARTIAL_TEMPLATE,
        {"request": request, "todo": todo},
    )


class UpdateTodoForm(Form):
    title: StringField = StringField(
        "Title", validators=[validators.Length(min=3, max=25)]
    )
    completed: BooleanField = BooleanField("Completed", default=False)


@router.patch("/{todo_id}")
async def update_todo(
    request: Request,
    todo_id: Annotated[int, Path()],
    db: DBDependency,
    current_user: LoggedInUser,
):
    form_data = await request.form()
    update_todo_form = UpdateTodoForm(**form_data)
    todo = db.query(db_models.Todo).filter(db_models.Todo.id == todo_id).first()
    if not todo:
        raise errors.TodoNotFoundError
    if todo.owner_id != current_user.id:
        raise errors.TodoNotOwnedError
    todo.title = update_todo_form.title.data
    todo.completed = update_todo_form.completed.data
    db.commit()
    db.refresh(todo)
    return templates.TemplateResponse(
        TODO_PARTIAL_TEMPLATE,
        {"request": request, "todo": todo},
    )


@router.delete("/{todo_id}")
async def delete_todo(
    request: Request,
    todo_id: Annotated[int, Path()],
    db: DBDependency,
    current_user: LoggedInUser,
):
    todo = db.query(db_models.Todo).filter(db_models.Todo.id == todo_id).first()
    if not todo:
        raise errors.TodoNotFoundError
    if todo.owner_id != current_user.id:
        raise errors.TodoNotOwnedError
    db.delete(todo)
    db.commit()
    return templates.TemplateResponse(
        TODO_PARTIAL_TEMPLATE,
        {"request": request, "todo": todo},
    )
