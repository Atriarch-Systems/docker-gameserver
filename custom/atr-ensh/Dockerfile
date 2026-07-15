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
# GAMESERVER must equal "{gameCode}server" (= atr-enshserver) so the deploy
# manifest generator's cron/preStop/config-lgsm paths line up with the script.
ENV GAMESERVER=atr-enshserver
ENV STEAM_COMPAT_DATA_PATH=/data/compatdata/2278520

WORKDIR /app

RUN mkdir -p /data/compatdata/2278520

# Custom Enshrouded LinuxGSM-compatible wrapper and defaults.
COPY custom/atr-ensh/atr-enshserver /app/atr-enshserver
COPY custom/atr-ensh/config/_default.cfg /app/lgsm/config-default/config-lgsm/atr-enshserver/_default.cfg
COPY custom/atr-ensh/config/enshrouded_server.json /app/config-default/enshrouded_server.json

RUN sed -i 's/\r$//' /app/atr-enshserver && \
    chmod +x /app/atr-enshserver && \
    mkdir -p /data/serverfiles /data/logs /data/backup

HEALTHCHECK --interval=1m --timeout=1m --start-period=2m --retries=1 CMD /app/entrypoint-healthcheck.sh || exit 1
