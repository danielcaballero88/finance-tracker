from pydoc import plain

import passlib.context as pc

pwd_context = pc.CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    result: bool = pwd_context.verify(plain_password, hashed_password)
    return result


def get_password_hash(password: str) -> str:
    result: str = pwd_context.hash(password)
    return result
