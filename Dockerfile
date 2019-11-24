FROM python:3.7.4

WORKDIR /app

RUN groupadd -g 1000 app && useradd -u 1000 -g app app && \
    chown app:app /app

COPY --chown=app:app ["requirenments.txt", "/app"]

RUN pip3 install --no-cache-dir -r requirenments.txt

USER app

COPY --chown=app:app [".", "/app"]
