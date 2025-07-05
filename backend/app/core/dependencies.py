from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.core.security import decode_access_token
from app.schemas.user import RoleEnum

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        return decode_access_token(token)
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

def require_role(role: RoleEnum):
    def checker(user=Depends(get_current_user)):
        if user.role != role and user.role != RoleEnum.ADMIN:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return checker
