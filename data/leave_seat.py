from core.supabase_client import supabase
from model.leave_seat import Place, LeaveSeatForm


def get_leaveSeat(date : str) :
    result = (
        supabase
        .table("leaveSeat")
        .select("*")
        .eq("date", date)
        .eq("status", "PENDING")
        .execute()
    )
    return result.data

def all_place() ->Place:
    result = supabase.table("place").select("*").execute()
    return result.data

def form_leaveSate(form : LeaveSeatForm) :

    for student in form.students :
        supabase.table("leave_seat").insert({
            "place_id": form.place_id,
            "student_id": student.id,
            "date": form.date,
            "period": form.period,
            "status": "PENDING"
        }).execute()

    return {"message": "success"}