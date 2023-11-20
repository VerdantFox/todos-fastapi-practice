from enum import Enum


class Role(str, Enum):
    UNAUTHENTICATED = "unauthenticated"
    USER = "user"
    ADMIN = "admin"
