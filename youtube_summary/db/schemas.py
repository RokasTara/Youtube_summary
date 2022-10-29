from pydantic import BaseModel


class SummaryBase(BaseModel):
    url: str


class SummaryCreate(SummaryBase):
    pass


class Summary(SummaryBase):
    id: int
    owner_id: int
    description: str
    transcript: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    summaries: list[Summary] = []

    class Config:
        orm_mode = True
