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