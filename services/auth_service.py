import bcrypt
from repositories.users_repository import (
    find_user_by_id,
    find_user_by_email
)


def authenticate_user(identifier: str, password: str):

    # Determine search method
    if identifier.isdigit():
        user = find_user_by_id(int(identifier))
    else:
        user = find_user_by_email(identifier)

    if not user:
        return None, "Invalid credentials"

    # Check password using bcrypt
    stored_hash = user["password"].encode("utf-8")
    entered = password.encode("utf-8")

    if not bcrypt.checkpw(entered, stored_hash):
        return None, "Invalid credentials"

    if user["active"] == 0:
        return None, "User is inactive"

    return user, None