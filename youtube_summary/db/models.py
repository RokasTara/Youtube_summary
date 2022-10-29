from enum import unique
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    summaries = relationship("Summary", back_populates="owner")


class Summary(Base):
    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    description = Column(String)
    url = Column(String, unique=True)
    transcript = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="summaries")
