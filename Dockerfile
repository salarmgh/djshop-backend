FROM python:3.7.4

WORKDIR /app

ENV DEPS="libpq-dev"
ENV TEMP_DEPS=""

RUN groupadd -g 1000 app && useradd -u 1000 -g app app && \
    chown app:app /app

COPY --chown=app:app ["requirenments.txt", "/app"]

RUN pip3 install --no-cache-dir -r requirenments.txt

COPY --chown=app:app [".", "/app"]

#RUN apk del --purge .build-deps

USER app

ENTRYPOINT ["uwsgi", "--uid", "app", "--gid", "app", \
"--chdir", "/app"]
