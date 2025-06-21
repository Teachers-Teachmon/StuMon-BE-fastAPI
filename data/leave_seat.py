from core.supabase_client import supabase
from model.leave_seat import Place, LeaveSeatForm
from model.student import Student


def get_leaveSeat(date: str):
    res = (
        supabase
        .table("leave_seat")
        .select(
            "period, "
            "place:place_id(name), "
            "student:student_id(student_number, name)"
        )
        .eq("date", date)
        .eq("status", "PENDING")
        .execute()
    )
    rows = res.data or []

    groups: dict[tuple[str, str], dict] = {}
    for r in rows:
        period = r["period"]
        place_name = r["place"]["name"]
        key = (period, place_name)

        if key not in groups:
            groups[key] = {
                "period":   period,
                "place":    place_name,
                "students": []
            }

        stu = r["student"]
        groups[key]["students"].append(f"{stu['student_number']} {stu['name']}")

    return {"data": list(groups.values())}

def all_place() ->Place:
    result = supabase.table("place").select("*").execute()
    return result.data

def form_leaveSate(student, form : LeaveSeatForm) :
    supabase.table("leave_seat").insert({
        "cause": form.cause,
        "place_id": form.place_id,
        "student_id": student.id,
        "date": form.date,
        "period": form.period,
        "status": "PENDING"
    }).execute()

    return {"message": "success"}


def update_leaveSeat(student : Student, form : LeaveSeatForm) :
    (supabase.table("leave_seat")
     .update({"status": "COMPLETED"})
     .eq("place_id", form.place_id)
     .eq("student_id", student.id)
     .eq("period", form.period)
     .eq("date", form.date)
     .execute())

def get_place_by_id(id : int) :
    result = supabase.table("place").select("*").eq("id", id).execute()
    return result.data