#
# Space Engineers Dedicated Server (Custom Scaffold) Dockerfile
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
ENV GAMESERVER=atrseserver
ENV STEAM_COMPAT_DATA_PATH=/data/compatdata/298740

WORKDIR /app

RUN mkdir -p /data/compatdata/298740

# Custom Space Engineers LinuxGSM-compatible wrapper scaffold.
COPY custom/atr-se/atrseserver /app/atrseserver
COPY custom/atr-se/config/_default.cfg /app/lgsm/config-default/config-lgsm/atrseserver/_default.cfg

RUN sed -i 's/\r$//' /app/atrseserver && \
    chmod +x /app/atrseserver && \
    mkdir -p /data/serverfiles /data/logs /data/backup

HEALTHCHECK --interval=1m --timeout=1m --start-period=2m --retries=1 CMD /app/entrypoint-healthcheck.sh || exit 1
