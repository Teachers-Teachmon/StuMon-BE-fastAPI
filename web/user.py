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

@router.get("/me")
def get_me(request: Request):
    token = request.cookies.get("access_token")
    user_id: int = decode_AT(token)["user_id"]
    return service.get_me(user_id)

@router.get("/login")
async def login(request : Request) :
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/callback")
async def auth_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)

    userinfo_response = await oauth.google.get(
        "https://www.googleapis.com/oauth2/v3/userinfo", token=token
    )
    user = userinfo_response.json()

    if service.callback(user, token) :
        email = user.get("email")
        name = user.get("name")
        picture = user.get("picture")

        access_token = token.get("id_token")

        user_id = data.get_user_id(email)
        payload = {
            "user_id": user_id,
            "email": email,
            "name": name,
            "picture": picture
        }

        jwt_token = create_AT(payload)
        url = os.getenv("FRONTEND_URL") + "auth"
        redirect_response = RedirectResponse(url=url)

        redirect_response.set_cookie(
            key="access_token",
            value=jwt_token,
            httponly=False,
            secure=False,  # 배포 시 True
            samesite="lax",
            max_age=3600  # 1시간 유효
        )

        return redirect_response
    return {"message": "User not found"}