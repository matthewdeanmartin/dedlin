FROM python:3.11.1-slim-buster
WORKDIR /app
ENV PIP_NO_CACHE_DIR=off
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=utf-8
ENV PATH="/root/.local/bin:${PATH}"
RUN python -m pip install --no-cache-dir --upgrade pip --quiet && \
    python -m pip install --user pipx && python -m pipx ensurepath && \
    pipx install "dedlin>=1.12.0"
ENTRYPOINT ["dedlin"]
