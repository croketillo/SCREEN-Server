###############################################################################
## Final image
###############################################################################
FROM alpine:3.18

LABEL maintainer="CROKETILLO (croketillo@gmail.com)

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONIOENCODING=utf-8 \
    PYTHONUNBUFFERED=1 \
    USER=app \
    UID=1000

RUN echo "**** install Python ****" && \
    apk add --update --no-cache \
            python3~=3.11 && \
    rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh ./src /app/

RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/${USER}" \
    --shell "/sbin/nologin" \
    --uid "${UID}" \
    "${USER}" && \
    chown -R app:app /app

WORKDIR /app
USER app

CMD ["/bin/sh", "/app/run.sh"]
