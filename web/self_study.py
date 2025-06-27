from fastapi import APIRouter, HTTPException, Query
from datetime import date
from service.self_study import self_study_service as service

router = APIRouter(prefix="/self-study")

@router.get("/stats")
def get_stats(
    start: date = Query(date(2025, 3, 4)),
    end:   date = Query(date(2025, 7, 23)),
):
    try:
        return service.stats(start, end)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/next")
def get_next():
    try:
        return service.next()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
