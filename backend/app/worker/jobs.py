from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from datetime import date
from app.db.session import SessionLocal
from app.models.issue import Issue, StatusEnum
from app.models.daily_stat import DailyStat

def collect_stats():
    db: Session = SessionLocal()
    try:
        today = date.today()
        stats = {
            StatusEnum.OPEN: 0,
            StatusEnum.TRIAGED: 0,
            StatusEnum.IN_PROGRESS: 0,
            StatusEnum.DONE: 0
        }

        for row in db.query(Issue.status).all():
            stats[row[0]] += 1

        existing = db.query(DailyStat).filter(DailyStat.date == today).first()
        if not existing:
            existing = DailyStat(date=today)
            db.add(existing)

        existing.open_count = stats[StatusEnum.OPEN]
        existing.triaged_count = stats[StatusEnum.TRIAGED]
        existing.in_progress_count = stats[StatusEnum.IN_PROGRESS]
        existing.done_count = stats[StatusEnum.DONE]

        db.commit()
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(collect_stats, "interval", minutes=30)
    scheduler.start()
