# app/api/deps.py
from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt  # JWTErrorを正しくインポート
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal
from app.models import User  # または import app.models as models を使用

# schemasモジュールが見つからないので、正しいパスを指定する必要があります
# 例えば、app.schemas から必要なものを直接インポート
from app.schemas.token import TokenPayload  # もしくはapp.schemas.token_schemaなど、実際のパスに合わせる

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login/access-token")


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
        token_data = TokenPayload(**payload)  # schemas. を削除
    except (JWTError, ValidationError):  # jose.jwt.JWTError → JWTError
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = db.query(User).filter(User.id == token_data.sub).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    # SQLAlchemyのColumnをブール値として評価できない問題を修正
    if current_user.is_active is not True:  # もしくは if current_user.is_active != True:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
