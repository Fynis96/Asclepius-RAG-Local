from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...core.security import create_access_token, create_refresh_token, verify_password
from ...crud.user import authenticate_user, update_user_refresh_token, get_user_by_refresh_token, get_user_by_email
from ...schemas.user import User, Token
from ..deps import get_current_user

router = APIRouter()

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token()
    update_user_refresh_token(db, user, refresh_token)
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}

@router.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    user = get_user_by_refresh_token(db, refresh_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    new_refresh_token = create_refresh_token()
    update_user_refresh_token(db, user, new_refresh_token)
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": new_refresh_token}

@router.post("/logout")
def logout(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    update_user_refresh_token(db, current_user, None)
    return {"detail": "Successfully logged out"}