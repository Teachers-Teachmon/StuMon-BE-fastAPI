from fastapi import APIRouter
from starlette.requests import Request
from utils.auth import decode_AT
from service import alert as service
router = APIRouter(prefix="/alert")

@router.get('')
def get_alert(request: Request) :
    token = request.cookies.get('access_token')
    user_id = decode_AT(token)["user_id"]
    return service.get_alert(user_id)

@router.post('/{alert_id}')
def update_alert(alert_id):
    return service.update_alert(alert_id)

@router.delete('')
def delete_alert(request: Request) :
    token = request.cookies.get('access_token')
    user_id = decode_AT(token)["user_id"]
    return service.delete_alert(user_id)