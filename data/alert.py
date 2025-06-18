from core.supabase_client import supabase
from model.alert import Alert


def sent_alert(leaveSeatAlert : Alert) :
    supabase.table("alert").insert({
        "title" : leaveSeatAlert.title,
        "content" : leaveSeatAlert.content,
        "recipient" : leaveSeatAlert.recipient,
        "is_read" : leaveSeatAlert.is_read
    }).execute()