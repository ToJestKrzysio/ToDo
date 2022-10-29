import re
from enum import Enum

from pydantic import BaseModel, validator


def validate_email(cls, email: str) -> str:
    """ Validates if email is correct. """
    regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if re.fullmatch(regex, email) is None:
        message = "Invalid email address."
        raise ValueError(message)
    return email


def validate_password_strength(cls, password: str) -> str:
    """
    Validates if password contains
      - 1 lower case letter
      - 1 upper case latter
      - 1 number
      - 10 characters
    """
    regex = r"(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-z\d!#$%^*]{10,40}"
    if re.fullmatch(regex, password) is None:
        message = "Password must contain lower case letter, upper case letter, number and 10 characters."
        raise ValueError(message)
    return password


class UserRegister(BaseModel):
    email: str
    name: str
    password: str

    validate_email = validator("email", allow_reuse=True)(validate_email)
    validate_password = validator("password", allow_reuse=True)(validate_password_strength)


class UserLogin(BaseModel):
    email: str
    password: str

    validate_email = validator("email", allow_reuse=True)(validate_email)
    validate_password = validator("password", allow_reuse=True)(validate_password_strength)


class TokenTypes(Enum):
    jwt = "JWT"


class TokenResponse(BaseModel):
    token: str
    type: TokenTypes
