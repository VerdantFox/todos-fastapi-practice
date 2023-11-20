# ----------- Auth Models -----------
from pydantic import BaseModel, EmailStr

from app import mixins
import app.web.field_types as ft
from app.permissions import Role


class UnauthenticatedUser(mixins.AuthUserMixin):
    """Unauthenticated User model"""

    id = -1
    username = "unauthenticated_user"
    is_active = False
    role = Role.UNAUTHENTICATED

    # non-table fields
    is_authenticated: bool = False


class CurrentUser(BaseModel, mixins.AuthUserMixin):
    """Current User model"""

    id: int
    email: EmailStr
    username: ft.Min3Field
    first_name: ft.Min3Field
    last_name: ft.Min3Field
    phone_number: ft.Min3Field | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


# ----------- User Models -----------
class UserFromAuth(BaseModel):
    id: int
    username: ft.Min3Field
    user_role: ft.Min3Field
