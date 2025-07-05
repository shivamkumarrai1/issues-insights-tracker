from sqlalchemy.orm import Session
from typing import List
from uuid import uuid4
from app.models.issue import Issue
from app.schemas.issue import IssueCreate, IssueUpdate
from app.models.user import RoleEnum

from app.services.sse_manager import sse_manager  # ✅ ADD THIS
import json  # ✅ For formatting the event payload


async def create_issue(db: Session, data: IssueCreate, reporter_id: str): 
    issue = Issue(
        id=str(uuid4()),
        title=data.title,
        description=data.description,
        file_path=data.file_path,
        severity=data.severity,
        reporter_id=reporter_id
    )
    db.add(issue)
    db.commit()
    db.refresh(issue)

    # ✅ BROADCAST EVENT (non-blocking)
    import asyncio
    asyncio.create_task(
        sse_manager.broadcast(json.dumps({
            "event": "issue_created",
            "issue_id": issue.id,
            "title": issue.title,
            "status": issue.status
        }))
    )

    return issue


def get_issue(db: Session, issue_id: str):
    return db.query(Issue).filter(Issue.id == issue_id).first()


def get_issues(db: Session, user_id: str, role: RoleEnum):
    if role in [RoleEnum.ADMIN, RoleEnum.MAINTAINER]:
        return db.query(Issue).all()
    return db.query(Issue).filter(Issue.reporter_id == user_id).all()


async def update_issue(db: Session, issue_id: str, data: IssueUpdate):
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        return None

    for field, value in data.dict(exclude_unset=True).items():
        setattr(issue, field, value)

    db.commit()
    db.refresh(issue)

    # ✅ Proper async broadcasting
    await sse_manager.broadcast(json.dumps({
        "event": "issue_updated",
        "issue_id": issue.id,
        "title": issue.title,
        "status": issue.status
    }))

    return issue



def delete_issue(db: Session, issue_id: str):
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        return False
    db.delete(issue)
    db.commit()
    return True
