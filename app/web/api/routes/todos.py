from typing import cast

from fastapi import APIRouter, status

from app.datastore import db_models as db_models
from app.datastore.database import DBDependency, Session
from app.web import auth
from app.web import field_types as ft
from app.web.api import api_models, errors

router = APIRouter(tags=["todos"], prefix="/todos")


# ----------- Todo routes -----------
@router.get(
    "", response_model=list[api_models.TodoOutLimited], status_code=status.HTTP_200_OK
)
async def get_todos(
    current_user: auth.TokenRequiredUser, db: DBDependency
) -> list[db_models.Todo]:
    """Get todos, filtering on the desired fields."""
    query = db.query(db_models.Todo)
    if not current_user.is_admin():
        query = query.filter(db_models.Todo.owner_id == current_user.id)
    return cast(list[db_models.Todo], query.all())


@router.get(
    "/{todo_id}", status_code=status.HTTP_200_OK, response_model=api_models.TodoOutFull
)
async def get_todo(
    current_user: auth.TokenRequiredUser, todo_id: ft.Id, db: DBDependency
) -> db_models.Todo:
    """Get a todo by id."""
    return _get_todo_by_id(current_user=current_user, todo_id=todo_id, db=db)


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=api_models.TodoOutFull
)
async def create_todo(
    current_user: auth.TokenRequiredUser,
    todo_in: api_models.TodoInPost,
    db: DBDependency,
) -> db_models.Todo:
    """Create a todo."""
    todo_model = db_models.Todo(
        title=todo_in.title,
        description=todo_in.description,
        priority=todo_in.priority,
        completed=todo_in.completed,
        owner_id=current_user.id,
    )
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model


@router.patch(
    "/{todo_id}", status_code=status.HTTP_200_OK, response_model=api_models.TodoOutFull
)
async def update_todo(
    current_user: auth.TokenRequiredUser,
    todo_id: ft.Id,
    todo_in: api_models.TodoInPatch,
    db: DBDependency,
) -> db_models.Todo:
    """Update a todo."""
    todo_model = _get_todo_by_id(current_user=current_user, todo_id=todo_id, db=db)
    for field, value in todo_in.model_dump(exclude_unset=True).items():
        setattr(todo_model, field, value)
    db.commit()
    db.refresh(todo_model)
    return todo_model


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    current_user: auth.TokenRequiredUser, todo_id: ft.Id, db: DBDependency
) -> None:
    """Delete a todo."""
    todo_model = _get_todo_by_id(current_user=current_user, todo_id=todo_id, db=db)
    db.delete(todo_model)
    db.commit()


# ------------ Helpers ------------
def _get_todo_by_id(
    current_user: db_models.User, todo_id: ft.Id, db: Session
) -> db_models.Todo:
    """Get a todo by id."""
    query = db.query(db_models.Todo).filter(db_models.Todo.id == todo_id)
    if not current_user.is_admin():
        query = query.filter(db_models.Todo.owner_id == current_user.id)
    if todo_model := query.first():
        return todo_model
    raise errors.TodoNotFoundError
