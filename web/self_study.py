from fastapi import APIRouter, HTTPException, Query, Header
from datetime import date

from starlette.requests import Request

from service.self_study import self_study_service as service
from utils.auth import decode_AT

router = APIRouter(prefix="/self-study")

@router.get("/stats")
def get_stats(
    request: Request,
    start: date = Query(date(2025, 3, 4)),
    end:   date = Query(date(2025, 7, 23)),
):
    token = request.cookies.get("access_token")
    user_id = decode_AT(token)["user_id"]
    try:
        return service.stats(user_id, start, end)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/next")
def get_next(request: Request):
    token = request.cookies.get("access_token")
    user_id = decode_AT(token)["user_id"]
    try:
        return service.next(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
