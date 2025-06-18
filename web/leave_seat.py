from fastapi import APIRouter, Body

from model.leave_seat import LeaveSeatForm
from service import leave_seat as service

router = APIRouter(prefix="/leaveseat")

@router.get("/place")
async def get_place() :
    return service.get_place()

@router.get("/")
async def get_leaveSeat(date : str) :
    return service.get_leaveSeat(date)


@router.post("/")
async def post_leaveSeat(form : LeaveSeatForm = Body(...)) :
    return service.form_leaveSate(form)

@router.post("/complete")
def complete_leaveSeat(form : LeaveSeatForm = Body(...)) :
    return service.complete_leaveSeat(form)