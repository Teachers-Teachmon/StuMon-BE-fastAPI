from fastapi import APIRouter
from service import alert as service
router = APIRouter(prefix="/alert")

@router.get('')
def get_alert() :
    return service.get_alert()

@router.post('/{alert_id}')
def update_alert(alert_id):
    return service.update_alert(alert_id)