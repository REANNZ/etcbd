FROM debian:bookworm

ENV FILEBEAT_VERSION=6.3.2

# make debconf use non-interactive mode:
ENV DEBIAN_FRONTEND=noninteractive

# Install curl & ca-certificates (first install apt-utils)
# Install locales needed to run localedef later
# Clean up apt temporary files
RUN apt-get update && \
    apt-get install -y apt-utils && \
    apt-get install -y ca-certificates curl --no-install-recommends && \
    apt-get -y install --no-install-recommends locales && \
    rm -rf /var/lib/apt/lists/*

# install envPlate
RUN curl -sLo /usr/local/bin/ep https://github.com/kreuzwerker/envplate/releases/download/1.0.0-RC1/ep-linux && chmod +x /usr/local/bin/ep

RUN curl -sLO https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-${FILEBEAT_VERSION}-amd64.deb && \
    dpkg -i filebeat-${FILEBEAT_VERSION}-amd64.deb && \
    rm -f filebeat-${FILEBEAT_VERSION}-amd64.deb

COPY filebeat.yml /etc/filebeat/filebeat.yml
# Copy in startup.d files
COPY content /

VOLUME /var/lib/filebeat

CMD ["/startup.sh", "/usr/bin/filebeat", "-e", "-c", "/etc/filebeat/filebeat.yml"]

