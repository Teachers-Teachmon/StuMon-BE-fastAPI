from core.supabase_client import supabase
import random

def get_students_by_partial_name(partial_name: str):
    print(partial_name)
    result = (
        supabase
        .table("student")
        .select("name, student_number")
        .ilike("name", f"%{partial_name}%")  # 대소문자 구분 없이 포함된 이름 검색
        .execute()
    )

    # name + number 조합으로 변환
    students = result.data

    combined = [f"{student['name']}({student['student_number']})" for student in students]
    return combined

def get_profile(username: str):
    result = (
        supabase
        .table("student")
        .select("name, student_number, profile_image")
        .eq("name", username)
        .single()
        .execute()
    )
    student = result.data
    print(student)
    sn = student["student_number"]
    grade = sn // 1000
    klass = (sn % 1000) // 100
    seat = sn % 100
    student_number = f"{grade}학년 {klass}반 {seat}번"
    return {
        "profile_image": student["profile_image"],
        "name": student["name"],
        "student_number": student_number,
    }

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