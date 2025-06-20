import os
import uvicorn
from fastapi import FastAPI, Request, Response
from starlette.middleware.cors import CORSMiddleware
import os
from web import user
from web import leave_seat
from web import alert
from starlette.middleware.sessions import SessionMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://stu-mon-fe.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=os.environ["SESSION_SECRET_KEY"])

app.add_middleware(SessionMiddleware, secret_key=os.environ["SESSION_SECRET_KEY"])
app.include_router(leave_seat.router)
app.include_router(user.router)
app.include_router(alert.router)

if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, reload=True)