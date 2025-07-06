import os

from fastapi import APIRouter
from fastapi.params import Query
from starlette.responses import RedirectResponse
from service import user as service
from fastapi import Request
from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv
from jose import jwt
from data import user as data
from fastapi import HTTPException

from utils.auth import create_AT, decode_AT

SECRET_KEY = os.getenv("JWT_SECRET_KEY")

router = APIRouter(prefix="/auth")


load_dotenv()

oauth = OAuth()
oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

@router.get("/")
async def search_user(q : str = Query):
    return service.search_user(q)

from fastapi import HTTPException

@router.get("/me")
def get_me(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="No token provided")

    try:
        decoded = decode_AT(token)
        user_id: int = decoded["user_id"]
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid or expired token: {e}")

    try:
        user_info = service.get_me(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"User retrieval failed: {e}")

    return user_info


@router.get("/login")
async def login(request : Request) :
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    return await oauth.google.authorize_redirect(request, redirect_uri)

from fastapi import Response

@router.get("/callback")
async def auth_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    userinfo_response = await oauth.google.get(
        "https://www.googleapis.com/oauth2/v3/userinfo", token=token
    )
    user = userinfo_response.json()

    email = user.get("email")
    name = user.get("name")
    picture = user.get("picture")

    user_id = data.get_user_id(email)

    payload = {
        "user_id": user_id,
        "email": email,
        "name": name,
        "picture": picture
    }

    # ✅ JWT 생성
    jwt_token = create_AT(payload)

    frontend_url = os.getenv("FRONTEND_URL")
    url = f"{frontend_url}/auth?token={jwt_token}"

    # ✅ RedirectResponse + Set-Cookie
    response = RedirectResponse(url=url)
    response.set_cookie(
        key="access_token",    # 쿠키 이름
        value=jwt_token,       # JWT 값
        httponly=False,         # JavaScript에서 접근 불가
        secure=True,           # HTTPS에서만 전송
        samesite="none"        # 크로스사이트 허용
    )

    return response