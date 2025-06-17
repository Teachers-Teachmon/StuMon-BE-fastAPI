# 사용하는 곳에서 from app.core.supabase_client import supabase
# 저렇게 불러와서 supabase.table("student").select("*").execute() 이런식으로 사용

import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)