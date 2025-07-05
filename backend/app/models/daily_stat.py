from sqlalchemy import Column, Date, Integer
from app.db.base import Base

class DailyStat(Base):
    __tablename__ = "daily_stats"

    date = Column(Date, primary_key=True)
    open_count = Column(Integer, default=0)
    triaged_count = Column(Integer, default=0)
    in_progress_count = Column(Integer, default=0)
    done_count = Column(Integer, default=0)
