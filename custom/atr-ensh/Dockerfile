#
# Enshrouded Dedicated Server (Custom) Dockerfile
#
# Fork: https://github.com/Atriarch-Systems/docker-gameserver
#
# Modifications Copyright (c) Atriarch Systems <postmaster@mail.atriarch.systems>
#

ARG ATR_CUSTOM_BASE_IMAGE=docker.atriarch.systems/lgsm-atr-custom-base:latest
FROM ${ATR_CUSTOM_BASE_IMAGE}

LABEL maintainer.fork="Atriarch Systems <postmaster@mail.atriarch.systems>"
LABEL game="Enshrouded"
LABEL shortname="atr-ensh"
ARG SHORTNAME=atr-ensh
ENV GAMESERVER=atrenshserver
ENV STEAM_COMPAT_DATA_PATH=/data/compatdata/2278520

WORKDIR /app

RUN mkdir -p /data/compatdata/2278520

# Custom Enshrouded LinuxGSM-compatible wrapper and defaults.
COPY custom/atr-ensh/atrenshserver /app/atrenshserver
COPY custom/atr-ensh/config/_default.cfg /app/lgsm/config-default/config-lgsm/atrenshserver/_default.cfg
COPY custom/atr-ensh/config/enshrouded_server.json /app/config-default/enshrouded_server.json

RUN sed -i 's/\r$//' /app/atrenshserver && \
    chmod +x /app/atrenshserver && \
    mkdir -p /data/serverfiles /data/logs /data/backup

HEALTHCHECK --interval=1m --timeout=1m --start-period=2m --retries=1 CMD /app/entrypoint-healthcheck.sh || exit 1
