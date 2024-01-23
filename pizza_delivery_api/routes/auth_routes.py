from fastapi import APIRouter, status
from ..models.connection.database import engine, Session
from ..models.schemas import SignUpModelRequest, SignUpModelResponse
from ..models.models import User
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash

auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

session = Session(bind=engine)

@auth_router.get('/')
async def hello():
    return { 'message': 'Hello, world' }

@auth_router.post('/signup', response_model=SignUpModelResponse,
                  status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModelRequest) -> SignUpModelResponse:
    db_email = session.query(User).filter(User.email == user.email).first()

    if db_email is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail='O usuário com esse e-mail já existe'
        )
        
    db_username = session.query(User).filter(User.username == user.username).first()

    if db_username is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail='O usuário com esse username já existe'
        )

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff
    )

    session.add(new_user)

    session.commit()

    return new_user