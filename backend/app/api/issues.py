from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.models.daily_stat import DailyStat
from app.schemas.daily_stat import DailyStatRead
from app.schemas.issue import IssueCreate, IssueRead, IssueUpdate
from app.core.dependencies import get_db, get_current_user
from app.crud import issue as crud
from app.models.user import RoleEnum

router = APIRouter()

@router.post("/", response_model=IssueRead)
async def create_issue(data: IssueCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return await crud.create_issue(db, data, user.user_id)

@router.get("/", response_model=List[IssueRead])
def list_issues(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return crud.get_issues(db, user.user_id, user.role)

@router.get("/{issue_id}", response_model=IssueRead)
def get_issue(issue_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    issue = crud.get_issue(db, issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    if user.role == RoleEnum.REPORTER and issue.reporter_id != user.user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return issue

@router.put("/{issue_id}", response_model=IssueRead)
async def update_issue(issue_id: str, data: IssueUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    issue = crud.get_issue(db, issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    if user.role == RoleEnum.REPORTER:
        raise HTTPException(status_code=403, detail="Forbidden")

    return await crud.update_issue(db, issue_id, data)


@router.delete("/{issue_id}")
def delete_issue(issue_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can delete")

    if not crud.delete_issue(db, issue_id):
        raise HTTPException(status_code=404, detail="Issue not found")
    
    return {"message": "Deleted"}
@router.get("/daily-stats", response_model=List[DailyStatRead])
def get_stats(db: Session = Depends(get_db)):
    return db.query(DailyStat).order_by(DailyStat.date.desc()).limit(30).all()
