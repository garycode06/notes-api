from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import create_token, password_hasher, verify_password
from app.database import get_db
from app.models.users import User
from app.schemas.auth import LoginRequest, RegisterRequest, Token
from app.schemas.users import UserResponse

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


def _get_user_by_login(db: Session, login: str) -> User | None:
    return db.query(User).filter(
        (User.username == login) | (User.email == login)
    ).first()


def _create_access_token(user: User) -> Token:
    access_token = create_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


def _authenticate_user(db: Session, login: str, password: str) -> User:
    user = _get_user_by_login(db, login)

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utilisateur ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.actif:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Utilisateur inactif",
        )

    return user


@auth_router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_data: RegisterRequest,
    db: Session = Depends(get_db),
):
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nom d'utilisateur ou email deja utilise",
        )

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=password_hasher(user_data.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@auth_router.post("/login", response_model=Token)
def login(
    user_data: LoginRequest,
    db: Session = Depends(get_db),
):
    user = _authenticate_user(db, user_data.username, user_data.password)
    return _create_access_token(user)


@auth_router.post("/token", response_model=Token)
def token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = _authenticate_user(db, form_data.username, form_data.password)
    return _create_access_token(user)
