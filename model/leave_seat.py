from typing import List, Optional
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
    place_name : Optional[str] = None
    date : str
    place_id : Optional[int] = None
    students : List[Student]
    period : str