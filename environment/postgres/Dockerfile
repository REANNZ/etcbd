ARG POSTGRES_OLD="9.5"
ARG POSTGRES_CUR="17"

FROM postgres:${POSTGRES_CUR}
ARG POSTGRES_OLD
ARG POSTGRES_CUR

# Install old PostgreSQL binaries (and basic utils - procps)
RUN apt-get update && \
    apt-get install -y --no-install-recommends postgresql-${POSTGRES_OLD} && \
    apt-get install -y procps && \
    rm -rf /var/lib/apt/lists/*

# use per-version data dir
ENV PGDATA="/var/lib/postgresql/data/${POSTGRES_CUR}"

# support older data with MD5 encryption (for authentication among our containers only)
ENV POSTGRES_HOST_AUTH_METHOD=md5

# create the dir for current version
RUN install --verbose --directory --owner postgres --group postgres --mode 0700 "$PGDATA"

COPY content /

# Override entrypoint
ENTRYPOINT ["/envwrap.sh", "/startup.sh", "docker-entrypoint.sh"]

# Reiterate the command - gets dropped when overriding ENTRYPOINT
CMD ["postgres"]
