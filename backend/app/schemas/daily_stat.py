from pydantic import BaseModel
from datetime import date

class DailyStatRead(BaseModel):
    date: date
    open_count: int
    triaged_count: int
    in_progress_count: int
    done_count: int

    class Config:
        orm_mode = True
