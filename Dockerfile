FROM python:3.8.2

WORKDIR /app

RUN groupadd -g 1000 app && useradd -u 1000 -g app app && \
    chown app:app /app

COPY ["requirenments.txt", "/app"]

RUN pip3 install --no-cache-dir -r requirenments.txt


COPY [".", "/app"]

RUN chown -R app:app /app

USER app
