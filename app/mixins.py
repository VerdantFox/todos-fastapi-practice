from app.permissions import Role


class AuthUserMixin:
    """Mixin for the User model."""

    # non-table fields
    role: Role
    is_authenticated: bool = True

    def is_admin(self) -> bool:
        return self.role == Role.ADMIN
