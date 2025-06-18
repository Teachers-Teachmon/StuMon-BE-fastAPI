from typing import List
from pydantic import BaseModel
from model.student import Student

class LeaveSeatReq(BaseModel) :
    day : str

class LeaveSeatRes(BaseModel) :
    place : str
    students : List[Student]
    period : str

class Place(BaseModel) :
    place_name : str
    place_id : int
    floor : int

class LeaveSeatForm(BaseModel) :
    cause : str
    place_id : int
    date : str
    students : List[Student]
    period : str