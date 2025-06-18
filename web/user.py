import os

from fastapi import APIRouter
from fastapi.params import Query
from starlette.responses import RedirectResponse
from service import user as service
from fastapi import Request
from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv

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
    print(token)
    access_token = token.get("id_token")

    if service.callback(user, token) :
        redirect_url = f"http://localhost:5173/?token={access_token}"
        return RedirectResponse(url=redirect_url)
    return {"message": "User not found"}