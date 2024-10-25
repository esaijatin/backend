# app/models.py
from pydantic import BaseModel

class Certificate(BaseModel):
    name: str
    course: str
    date: str
    qr_code: str
