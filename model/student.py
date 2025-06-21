from pydantic import BaseModel


class Student(BaseModel) :
    name : str
    student_number : int