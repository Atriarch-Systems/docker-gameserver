#
# Space Engineers Dedicated Server (Custom) Dockerfile
#
# Fork: https://github.com/Atriarch-Systems/docker-gameserver
#
# Modifications Copyright (c) Atriarch Systems <postmaster@mail.atriarch.systems>
#

ARG ATR_CUSTOM_BASE_IMAGE=docker.atriarch.systems/lgsm-atr-custom-base:latest
FROM ${ATR_CUSTOM_BASE_IMAGE}

LABEL maintainer.fork="Atriarch Systems <postmaster@mail.atriarch.systems>"
LABEL game="Space Engineers"
LABEL shortname="atr-se"
ARG SHORTNAME=atr-se
# GAMESERVER must equal "{gameCode}server" (= atr-seserver) so the deploy
# manifest generator's cron/preStop/config-lgsm paths line up with the script.
ENV GAMESERVER=atr-seserver
ENV STEAM_COMPAT_DATA_PATH=/data/compatdata/298740

WORKDIR /app

RUN mkdir -p /data/compatdata/298740

# Custom Space Engineers LinuxGSM-compatible wrapper and defaults.
COPY custom/atr-se/atr-seserver /app/atr-seserver
COPY custom/atr-se/config/_default.cfg /app/lgsm/config-default/config-lgsm/atr-seserver/_default.cfg

RUN sed -i 's/\r$//' /app/atr-seserver && \
    chmod +x /app/atr-seserver && \
    mkdir -p /data/serverfiles /data/logs /data/backup

HEALTHCHECK --interval=1m --timeout=1m --start-period=2m --retries=1 CMD /app/entrypoint-healthcheck.sh || exit 1
