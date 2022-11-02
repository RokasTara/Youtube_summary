from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from youtube_summary.db import schemas, crud
from youtube_summary.utils.utils import get_db, get_transcript, get_summary

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get("/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/{user_id}/summaries/", response_model=schemas.Summary)
def create_summary_for_user(
        user_id: int, summary: schemas.SummaryCreate, db: Session = Depends(get_db)
):
    transcript = get_transcript(summary.url)
    description = get_summary(transcript)
    return crud.create_summary(db=db, summary=summary, user_id=user_id, description=description, transcript=transcript)
