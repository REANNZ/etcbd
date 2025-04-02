FROM postgres:9.5
COPY content /

# Override entrypoint
ENTRYPOINT ["/envwrap.sh", "/startup.sh", "docker-entrypoint.sh"]

# Reiterate the command - gets dropped when overriding ENTRYPOINT
CMD ["postgres"]
