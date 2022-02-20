"""Password utility module."""

import passlib.context as pc

pwd_context = pc.CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies if a password matches the stored hash."""
    result: bool = pwd_context.verify(plain_password, hashed_password)
    return result


def get_password_hash(password: str) -> str:
    """Given a password, returns the corresponding hash."""
    result: str = pwd_context.hash(password)
    return result
