from data import leave_seat as data
from model.leave_seat import LeaveSeatForm


def get_leaveSeat(date : str) :
    return data.get_leaveSeat(date)


def get_place() :
    return data.all_place()

def form_leaveSate(form : LeaveSeatForm) :
    return data.form_leaveSate(form)