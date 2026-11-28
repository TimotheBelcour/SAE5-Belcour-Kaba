FROM python:3.13-slim-bookworm AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app
RUN useradd --create-home --uid 1000 django \
    && mkdir /app/staticfiles \
    && chown django:django /app/staticfiles

# En local, le code et les dépendances viennent des volumes de l'override.
FROM base AS development
USER django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Les dépendances sont installées avant de copier le code pour garder le cache Docker.
FROM base AS dependencies
COPY app/requirements.txt .
RUN python -m venv /opt/venv \
    && pip install --no-cache-dir -r requirements.txt

FROM base AS production
COPY --from=dependencies /opt/venv /opt/venv
COPY --chown=django:django app/ .
USER django
EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--access-logfile", "-"]
