from core.supabase_client import supabase
from model.leave_seat import Place, LeaveSeatForm
from model.student import Student


def get_leaveSeat(date: str):
    res = (
        supabase
        .table("leave_seat")
        .select(
            "period, "
            "status, "  
            "place:place_id(name), "
            "student:student_id(student_number, name)"
        )
        .eq("date", date)
        .execute()
    )
    print(res.data)
    rows = res.data or []

    groups: dict[tuple[str, str], dict] = {}
    for r in rows:
        period = r["period"]
        place_name = r["place"]["name"]
        status = r["status"]
        key = (period, place_name)

        if key not in groups:
            groups[key] = {
                "period":   period,
                "place":    place_name,
                "status":   status,    # 여기 추가!
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

def from_name_to_id(name: str) :
    result = supabase.table("place").select("id").eq("name", name).execute()
    print(result.data)
    return result.data[0]["id"]

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

def get_place_id(name: str) :
    result = supabase.table("place").select("id").eq("name", name).execute()
    return result.data[0]["id"]