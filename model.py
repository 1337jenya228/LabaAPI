from typing import List
from pydantic import BaseModel
from datetime import datetime

class textNotes(BaseModel):
    id: int
    text: str = None

class infoNotes(BaseModel):
    creat: datetime
    updated: datetime

class createNotes(BaseModel):
    id: int

class listNotes(BaseModel):
    notes_list:List[int]