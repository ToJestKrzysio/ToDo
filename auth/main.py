from fastapi import FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from lib import logger
from lib.fastapi_generics import MessageResponse, HTTPExceptionResponseModel

from auth.models import UserRegister, UserLogin, TokenResponse, TokenTypes
from auth.utils import hash_password, validate_password, create_token
from auth.db import User, session_maker

app = FastAPI()


@app.post(
    path="/register",
    status_code=201,
    responses={
        201: {"model": MessageResponse},
        404: {"model": HTTPExceptionResponseModel},
    }
)
async def register(user_data: UserRegister) -> MessageResponse:
    logger.info(f"Creating new user {user_data.email}.")

    with session_maker() as session:
        new_user = User(
            name=user_data.name,
            email=user_data.email,
            password_hash=hash_password(user_data.password)
        )
        session.add(new_user)

        try:
            session.commit()
        except IntegrityError:
            message = f"User {user_data.email} already exists."
            logger.error(message)
            raise HTTPException(status_code=404, detail=message)

    message = f"Successfully created user {user_data.email}."
    return MessageResponse(message=message)


@app.post(
    path="/login",
    status_code=200,
    responses={
        200: {"model": TokenResponse},
        401: {"model": HTTPExceptionResponseModel},
        404: {"model": HTTPExceptionResponseModel},
    }
)
async def login(user_login: UserLogin) -> TokenResponse:
    logger.info(f"Processing user {user_login.email} login.")

    with session_maker() as session:
        user, *_ = session.execute(select(User).where(User.email == user_login.email)).first()

        if user is None:
            message = f"User {user_login.email} does not exist."
            logger.error(message)
            raise HTTPException(status_code=404, detail=message)

        if validate_password(password=user_login.password, password_hash=user.password_hash) is False:
            message = f"Invalid credentials for user {user_login.email}."
            logger.error(message)
            raise HTTPException(status_code=401, detail=message)

        token = create_token(sub=user.id)
        logger.info(f"Login of user {user_login.email} succeeded.")
        return TokenResponse(token=token, type=TokenTypes.jwt)
