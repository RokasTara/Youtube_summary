from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from db import crud, models, schemas
from db.database import SessionLocal, engine
from youtube_summary.utils.utils import get_summary, get_transcript

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/summaries/", response_model=schemas.Summary)
def create_sumamry_for_user(
    user_id: int, summary: schemas.SummaryCreate, db: Session = Depends(get_db)
):
    transcript = get_transcript(summary.url)
    description = get_summary(transcript)
    return crud.create_summary(db=db, summary=summary, user_id=user_id, description=description, transcript=transcript)


@app.get("/summaries/", response_model=list[schemas.Summary])
def read_summaries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    summaries = crud.get_summaries(db, skip=skip, limit=limit)
    return summaries

# get summary by id

@app.get("/summaries/{summary_id}", response_model=schemas.Summary)
def read_summary(summary_id: int, db: Session = Depends(get_db)):
    db_summary = crud.get_summary(db, summary_id=summary_id)
    if db_summary is None:
        raise HTTPException(status_code=404, detail="Summary not found")
    return db_summary
