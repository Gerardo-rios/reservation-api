FROM python:3.12.4-alpine3.20

WORKDIR /app

RUN apk add --no-cache gcc musl-dev libffi-dev

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir pipx && \
    pipx install poetry && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi && \
    poetry run uvicorn --version

COPY . .

ENV PYTHONPATH=/app:$PYTHONPATH

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]