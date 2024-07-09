FROM python:3.12.4-alpine3.20

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install pipx && \
    pipx install poetry && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

RUN poetry install --no-dev

COPY . .

CMD ["uvicorn", "src.infraestructure.framework.fastapi.main:app", "--host", "0.0.0.0", "--port", "8000"]