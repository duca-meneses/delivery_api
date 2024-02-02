from os import access
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from pizza_delivery_api.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)

from ..models.connection.database import get_session
from ..models.models import User
from ..models.schemas import SignUpModelRequest, SignUpModelResponse, Token

auth_router = APIRouter(prefix='/auth', tags=['auth'])

OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
Session = Annotated[Session, Depends(get_session)]


@auth_router.get('/')
async def hello():
    return {'message': 'Hello, world'}


@auth_router.post(
    '/signup',
    response_model=SignUpModelResponse,
    status_code=status.HTTP_201_CREATED,
)
async def signup(
    user: SignUpModelRequest, session: Session
) -> SignUpModelResponse:
    db_email = session.scalar(select(User).where(User.email == user.email))
    if db_email is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='O usuário com esse e-mail já existe',
        )

    db_username = session.scalar(
        select(User).where(User.username == user.username)
    )

    if db_username is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='O usuário com esse username já existe',
        )

    hashed_password = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        is_active=user.is_active,
        is_staff=user.is_staff,
    )

    session.add(new_user)

    session.commit()

    return new_user


@auth_router.post('/token', response_model=Token)
def login_for_access_token(form_data: OAuth2Form, session: Session):
    user = session.scalar(
        Select(User).where(
            User.email == form_data.username
            or User.username == form_data.username
        )
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect (email, username) or password',
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect (email or username) or password',
        )

    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}


@auth_router.post('/refresh_token', response_model=Token)
def refresh_token(user: Annotated[User, Depends(get_current_user)]):
    new_access_token = create_access_token(data={'sub': user.email})

    return {'access_token': new_access_token, 'token_type': 'bearer'}
