from data import leave_seat as data
from data import alert
from model.alert import AlertRes
from model.leave_seat import LeaveSeatForm


def get_leaveSeat(date : str) :
    return data.get_leaveSeat(date)


def get_place() :
    return data.all_place()

def form_leaveSate(form: LeaveSeatForm):
    place_id = data.from_name_to_id(form.place_name)
    form.place_id = place_id
    for student in form.students:
        data.form_leaveSate(student, form)  # 동기 함수 호출


def complete_leaveSeat(form: LeaveSeatForm):
    place = data.get_place_by_id(form.place_id)

    period = ""
    if form.period == "SEVEN" :
        period = "7교시"
    if form.period == "EIGHT_NIGHT" :
        period = "8~9교시"
    if form.period == "TEN_ELEVEN" :
        period = "10~11교시"

    for student in form.students:
        data.update_leaveSeat(student, form)
        leaveSeatAlert = AlertRes(
            title="이석 신청이 완료되었어요!",
            content=f"{form.date} {period} '{place[0]["name"]}'에 이석이 완료되었습니다!",
            recipient=student.id,
            is_read=False
        )
        alert.sent_alert(leaveSeatAlert)

    return {"message": "처리 완료"}

def get_place_id(name: str) :
    return data.get_place_id(name)