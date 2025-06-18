from fastapi import Request
from data import user as data
import os
from starlette.responses import RedirectResponse

import random

def search_user(username : str) :
    return data.get_students_by_partial_name(username)

def get_profile(username: str):
    return data.get_profile(username)

async def callback(user, token) :

    email = user.get("email")
    name = user.get("name")
    picture = user.get("picture")
    google_id = user.get("sub")

    return data.create_student(email, name, google_id, picture)
    # student_number = email.split("@")[0] if email else None