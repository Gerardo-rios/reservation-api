FROM python:3.12

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev

COPY ./src ./src

CMD ["uvicorn", "src.infrastructure.framework.fastapi.main:app", "--host", "0.0.0.0", "--port", "8000"]