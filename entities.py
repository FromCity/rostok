from pydantic import BaseModel
import datetime


class Prompt(BaseModel):
    id: int
    prompt: str
    version: int
    adding_datetime: datetime.datetime

    class Config:
        orm_mode = True