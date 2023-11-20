from pydantic import BaseModel, EmailStr, Field

from app.web import field_types as ft
from app.permissions import Role


# ----------- User Models -----------
class UserInPost(BaseModel):
    email: EmailStr
    username: ft.Min3Field
    first_name: ft.Min3Field
    last_name: ft.Min3Field
    password: ft.Min8Field


class UserInPatch(BaseModel):
    email: EmailStr | None = None
    username: ft.Min3Field | None = None
    first_name: ft.Min3Field | None = None
    last_name: ft.Min3Field | None = None
    password: ft.Min8Field | None = None
    role: Role | None = None
    is_active: bool | None = None


class UserOutLimited(BaseModel):
    id: int = -1
    email: EmailStr = "unauthenticated@email.com"
    username: ft.Min3Field = "unauthenticated"
    first_name: ft.Min3Field = "unauthenticated"
    last_name: ft.Min3Field = "unauthenticated"
    role: Role = Role.UNAUTHENTICATED
    is_active: bool = False


# ----------- Todo Models -----------
class TodoInPost(BaseModel):
    title: ft.Min3Field
    description: ft.Min3Max100Field
    priority: ft.PriorityField
    completed: bool


class TodoInPatch(BaseModel):
    title: ft.Min3Field | None = None
    description: ft.Min3Max100Field | None = None
    priority: ft.PriorityField | None = None
    completed: bool | None = None


class TodoOutLimited(BaseModel):
    id: int
    title: ft.Min3Field
    description: ft.Min3Max100Field
    priority: ft.PriorityField
    completed: bool


# ----------- Full Models -----------
class TodoOutFull(TodoOutLimited):
    owner: UserOutLimited


class UserOutFull(UserOutLimited):
    todos: list[TodoOutLimited] = Field(default_factory=list)
