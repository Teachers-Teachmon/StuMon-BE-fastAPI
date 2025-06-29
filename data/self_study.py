from core.supabase_client import supabase

def get_self_study_weekdays(user_id: int) -> list[str]:
    res = (
        supabase
        .table("after_school")
        .select("day")
        .eq("type", "SELF_STUDY")
        .eq("s_id", user_id)
        .execute()
    )
    print(res)
    return [r["day"] for r in res.data]
