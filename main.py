import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from web import user
from web import leaveseat
from starlette.middleware.sessions import SessionMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=os.environ["SESSION_SECRET_KEY"])
app.include_router(leaveseat.router)
app.include_router(user.router)

if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, reload=True)