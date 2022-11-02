from fastapi import FastAPI

from db import models
from db.database import engine
from endpoints import summaries, users

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
app.include_router(users.router)
app.include_router(summaries.router)
