from datetime import datetime, timedelta
from uuid import UUID

import bcrypt
import jwt
from jwt import InvalidSignatureError, ExpiredSignatureError, DecodeError

from lib import logger, load_file, get_env

_ALGORITHM = "RS256"


def create_token(sub: str | UUID) -> str:
    """ Create JWT token for given user. """
    private_key = load_file(get_env("JWT_PRIVATE_KEY"))
    ttl = int(get_env("JWT_TTL"))
    exp = datetime.now() + timedelta(seconds=ttl)
    sub = sub if isinstance(sub, str) else str(sub)
    payload = {"sub": sub, "exp": exp.timestamp()}

    return jwt.encode(
        payload=payload,
        key=private_key,
        algorithm=_ALGORITHM,
    )


def validate_token(token: str) -> str:
    """ Checks token validity and returns token subject. """
    public_key = load_file(get_env("JWT_PUBLIC_KEY"))
    logger.info(f"Validating token '{token}'.")

    try:
        token_data = jwt.decode(
            token,
            key=public_key,
            algorithm=_ALGORITHM,
            options={"require": ["exp", "sub"]},
        )

    except ExpiredSignatureError:
        message = f"Expired token '{token}'."
        logger.error(message)
        raise ValueError(message)

    except (InvalidSignatureError, DecodeError):
        message = f"Invalid token '{token}'."
        logger.error(message)
        raise ValueError(message)

    logger.info(f"Token '{token}' valid.")
    return token_data["sub"]


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("UTF-8"), salt=bcrypt.gensalt()).decode("UTF-8")


def validate_password(password: str, password_hash: str) -> bool:
    """ Checks if provided password and password hash match. """
    return bcrypt.checkpw(password.encode("UTF-8"), password_hash.encode("UTF-8"))
