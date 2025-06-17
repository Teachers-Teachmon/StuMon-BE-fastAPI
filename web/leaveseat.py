from fastapi import APIRouter

router = APIRouter(prefix="/leaveseat")

@router.get("/")
async def get_leaveSeat() :
    return {"message" : "Hello World"}


@router.post("/")
async def post_leaveSeat(seat_id : int) :
    return {"message" : f"seat_id : {seat_id}"}

