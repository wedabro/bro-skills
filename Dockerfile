FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN useradd --create-home --uid 10001 appuser

COPY pyproject.toml README.md LICENSE ./
COPY bro_skills ./bro_skills
COPY tests ./tests
COPY .agent/skills ./.agent/skills
COPY .agent/workflows ./.agent/workflows

RUN pip install --no-cache-dir ".[test]"

USER appuser

CMD ["pytest", "-q", "-p", "no:cacheprovider"]
