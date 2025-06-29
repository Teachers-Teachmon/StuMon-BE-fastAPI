from core.supabase_client import supabase
import random

def get_students_by_partial_name(partial_name: str):
    print(partial_name)
    result = (
        supabase
        .table("student")
        .select("*")
        .ilike("name", f"%{partial_name}%")  # 대소문자 구분 없이 포함된 이름 검색
        .execute()
    )

    students = result.data
    combined = [{"name": student["name"], "student_number": student["student_number"], "id" : student['id']} for student in students]
    return combined


async def create_student(email: str, name: str, google_id: str, picture: str):

    def generate_student_number():
        return str(random.randint(100000, 999999))  # 6자리 숫자 문자열

    student_number = generate_student_number()
    existing_user = supabase.table("student").select("*").eq("email", email).execute()

    if not existing_user.data:
        supabase.table("student").insert({
            "email": email,
            "name": name,
            "profile_image": picture,
            "google_id": google_id,
            "student_number": student_number
        }).execute()

    return True

def get_user_id(email: str):
    result = supabase.table("student").select("id").eq("email", email).execute()
    return result.data[0]["id"]


def get_me(user_id):
    result = (
        supabase
        .table("student")
        .select("student_number")
        .eq("id", user_id)
        .single()
        .execute()
    )
    student = result.data
    sn = student["student_number"]
    grade = sn // 1000
    klass = (sn % 1000) // 100
    seat = sn % 100
    student_number = f"{grade}학년 {klass}반 {seat}번"

    after_school_res = (
        supabase
        .table("after_school")
        .select("t_name, period, place(name), name, day")
        .in_("type", ["AFTER_SCHOOL", "SELF_STUDY"])
        .eq("s_id", user_id)
        .execute()
    )
    rows = after_school_res.data or []

    DAYS = ["MON", "TUE", "WED", "THU"]
    schedule: dict[str, dict[str, dict]] = {d: {} for d in DAYS}

    for r in rows:
        day = r["day"]
        period = r["period"]
        place_name = r["place"]["name"]

        if day in schedule:
            schedule[day][period] = {
                "t_name": r["t_name"],
                "name": r["name"],
                "place": place_name,
            }

    return {
        "student_number": student_number,
        "after_school": schedule
    }