from core.supabase_client import supabase

def get_self_study_weekdays() -> list[str]:
    res = (
        supabase
        .table("after_school")
        .select("day")
        .eq("type", "SELF_STUDY")
        .execute()
    )
    return [r["day"] for r in res.data]
