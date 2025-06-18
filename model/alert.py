from pydantic import BaseModel



class AlertRes(BaseModel):
    title : str
    content : str
    recipient : int
    is_read : bool

class Alert(BaseModel) :
    title: str
    content: str

