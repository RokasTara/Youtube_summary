from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from youtube_summary.db import schemas, crud
from youtube_summary.utils.utils import get_db

router = APIRouter(
    prefix="/summaries",
    tags=["summaries"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.Summary])
def read_summaries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    summaries = crud.get_summaries(db, skip=skip, limit=limit)
    return summaries


@router.get("/{summary_id}", response_model=schemas.Summary)
def read_summary(summary_id: int, db: Session = Depends(get_db)):
    db_summary = crud.get_summary(db, summary_id=summary_id)
    if db_summary is None:
        raise HTTPException(status_code=404, detail="Summary not found")
    return db_summary
