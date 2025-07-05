# app/api/users.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
def list_users():
    return {"message": "User list will appear here."}
