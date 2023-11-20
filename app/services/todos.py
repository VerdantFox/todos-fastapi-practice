from typing import cast

from sqlalchemy.orm import Session

from app.datastore import db_models


async def get_todos_list(db: Session, current_user: db_models.User):
    query = db.query(db_models.Todo).filter(db_models.Todo.owner_id == current_user.id)
    return cast(list[db_models.Todo], query.all())


async def add_todo(db: Session, current_user: db_models.User, title: str):
    todo = db_models.Todo(
        title=title,
        description="Doesn't matter...",
        priority=1,
        owner_id=current_user.id,
        completed=False,
    )
    db.add(todo)
    db.commit()
    return todo
