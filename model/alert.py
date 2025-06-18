from pydantic import BaseModel

class Alert(BaseModel) :
    title: str
    content: str