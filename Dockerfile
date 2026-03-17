FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ENV MPLBACKEND=Agg
ENV MPLCONFIGDIR=/tmp/matplotlib

WORKDIR /app
COPY . /app

# Web app for click/tap-triggered renders.
CMD ["uv", "run", "--with", "fastapi", "--with", "uvicorn", "uvicorn", "web_app:app", "--host", "0.0.0.0", "--port", "8000"]
