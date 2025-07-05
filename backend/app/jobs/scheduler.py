from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from datetime import date
from app.db.session import SessionLocal
from app.models.issue import Issue
from app.models.daily_stat import DailyStat
from app.schemas.issue import StatusEnum

def aggregate_issue_stats():
    db: Session = SessionLocal()
    try:
        today = date.today()

        # Count issues by status
        status_counts = {
            status: db.query(Issue).filter(Issue.status == status).count()
            for status in StatusEnum
        }

        # Either update existing or insert new
        stat = db.query(DailyStat).filter(DailyStat.date == today).first()
        if not stat:
            stat = DailyStat(date=today)

        stat.open_count = status_counts.get(StatusEnum.OPEN, 0)
        stat.triaged_count = status_counts.get(StatusEnum.TRIAGED, 0)
        stat.in_progress_count = status_counts.get(StatusEnum.IN_PROGRESS, 0)
        stat.done_count = status_counts.get(StatusEnum.DONE, 0)

        db.merge(stat)
        db.commit()
        print(f"[SCHEDULER] Stats updated at {today}: {status_counts}")
    except Exception as e:
        print("[SCHEDULER ERROR]", e)
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(aggregate_issue_stats, 'interval', minutes=30)
    scheduler.start()
    print("[SCHEDULER] Background job started")
