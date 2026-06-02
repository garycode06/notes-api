from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_active_user
from app.core.security import password_hasher, verify_password
from app.database import get_db
from app.models.users import User
from app.schemas.users import PasswordUpdate, UserResponse, UserUpdate

users_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


def _ensure_unique_user_fields(
    db: Session,
    current_user: User,
    username: str | None = None,
    email: str | None = None,
) -> None:
    conditions = []
    if username is not None:
        conditions.append(User.username == username)
    if email is not None:
        conditions.append(User.email == email)
    if not conditions:
        return

    existing_user = db.query(User).filter(or_(*conditions)).first()
    if existing_user and existing_user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nom d'utilisateur ou email deja utilise",
        )


@users_router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_active_user),
):
    return current_user


@users_router.patch("/me", response_model=UserResponse)
def update_me(
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    update_data = user_data.model_dump(exclude_unset=True)

    _ensure_unique_user_fields(
        db=db,
        current_user=current_user,
        username=update_data.get("username"),
        email=update_data.get("email"),
    )

    if "username" in update_data:
        current_user.username = update_data["username"]
    if "email" in update_data:
        current_user.email = update_data["email"]

    db.commit()
    db.refresh(current_user)
    return current_user


@users_router.patch("/me/password", status_code=status.HTTP_204_NO_CONTENT)
def update_my_password(
    password_data: PasswordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mot de passe actuel incorrect",
        )

    current_user.hashed_password = password_hasher(password_data.new_password)
    db.commit()
    return None


@users_router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_me(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    db.delete(current_user)
    db.commit()
    return None
