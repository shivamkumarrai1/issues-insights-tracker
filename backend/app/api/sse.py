from fastapi import APIRouter, Request
from app.services.sse_manager import sse_manager

router = APIRouter()

@router.get("/api/stream")
async def stream_updates(request: Request):
    return await sse_manager.stream(request)
