FROM python:3.10

WORKDIR /api

RUN pip install poetry
COPY . /api

COPY ./pyproject.toml ./poetry.lock* /api/

RUN poetry config virtualenvs.create false
RUN poetry env use system
RUN poetry install

WORKDIR /api/youtube_summary/migrations
CMD ["alembic", "upgrade", "heads"]

WORKDIR /api/youtube_summary
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]