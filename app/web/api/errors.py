from fastapi import HTTPException, status

# ----------- User Errors -----------
UserNotFoundError = HTTPException(status_code=404, detail="User not found")
UserNotAuthenticatedError = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
)
UserNotValidatedError = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to validate user from JWT"
)
UserPermissionsError = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="User does not have permission to perform this action",
)

# ----------- Todo Errors -----------
TodoNotFoundError = HTTPException(status_code=404, detail="Todo not found")
