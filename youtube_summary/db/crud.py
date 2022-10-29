from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_summaries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Summary).offset(skip).limit(limit).all()


def create_summary(db: Session, summary: schemas.SummaryCreate, user_id: int, description: str, transcript: str):
    db_item = models.Summary(**summary.dict(), owner_id=user_id, description=description, transcript=transcript)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_summary(db: Session, summary_id: int):
    return db.query(models.Summary).filter(models.Summary.id == summary_id).first()
