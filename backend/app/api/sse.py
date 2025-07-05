from app.services.sse_manager import sse_manager
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

router = APIRouter()

@router.get("/")
async def stream(request: Request):
    return await sse_manager.stream(request)

