from core.supabase_client import supabase
from model.alert import AlertRes


def sent_alert(leaveSeatAlert : AlertRes) :
    supabase.table("alert").insert({
        "title" : leaveSeatAlert.title,
        "content" : leaveSeatAlert.content,
        "recipient" : leaveSeatAlert.recipient,
        "is_read" : leaveSeatAlert.is_read
    }).execute()
    
def get_alert(user_id) :
    result = (
        supabase
        .table("alert")
        .select("id, title, content, is_read")
        .eq("recipient", user_id)
        .execute()
    )
    return result.data

def update_alert(alert_id: int) :
    result = (
        supabase
        .table("alert")
        .update({"is_read": True})
        .eq("id", alert_id)
        .execute()
    )
    return {
        "message": "success"
    }


def delete_alert(user_id):
    result = (
        supabase
        .table("alert")
        .delete()
        .eq("recipient", user_id)
        .execute()
    )
    return {
        "message": "success"
    }