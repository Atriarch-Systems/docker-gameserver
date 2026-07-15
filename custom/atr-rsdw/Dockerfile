#
# RuneScape: Dragonwilds Dedicated Server (Custom, linux-native) Dockerfile
#
# Fork: https://github.com/Atriarch-Systems/docker-gameserver
#
# Modifications Copyright (c) Atriarch Systems <postmaster@mail.atriarch.systems>
#
# Runtime class: linux-native. Jagex ships a native 64-bit Linux dedicated
# server (Steam app 4019830, anonymous download), so this image builds directly
# on the LinuxGSM base -- which already provides SteamCMD -- and needs NO Proton
# custom base. See CONTRIBUTING-custom-games.md.
#

ARG LGSM_BASE_IMAGE=docker.atriarch.systems/linuxgsm:ubuntu-24.04
FROM ${LGSM_BASE_IMAGE}

LABEL maintainer.fork="Atriarch Systems <postmaster@mail.atriarch.systems>"
LABEL game="RuneScape: Dragonwilds"
LABEL shortname="atr-rsdw"
LABEL atriarch.custom="true"
LABEL atriarch.runtime="linux-native"
ARG SHORTNAME=atr-rsdw
# GAMESERVER must equal "{gameCode}server" (= atr-rsdwserver) so the deploy
# manifest generator's cron/preStop/config-lgsm paths line up with the script.
ENV GAMESERVER=atr-rsdwserver

WORKDIR /app

# 32-bit libs for SteamCMD + the native server's shared-library loader.
# The LinuxGSM/SteamCMD base already provides most of these, so on a warm base
# this is close to a no-op; it is kept explicit for reproducibility.
RUN dpkg --add-architecture i386 && \
    apt-get update && \
    apt-get install --no-install-recommends -y \
      ca-certificates \
      curl \
      lib32gcc-s1 \
      libc6:i386 \
      libstdc++6:i386 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Custom RuneScape: Dragonwilds LinuxGSM-compatible wrapper and defaults.
COPY custom/atr-rsdw/atr-rsdwserver /app/atr-rsdwserver
COPY custom/atr-rsdw/config/_default.cfg /app/lgsm/config-default/config-lgsm/atr-rsdwserver/_default.cfg

RUN sed -i 's/\r$//' /app/atr-rsdwserver && \
    chmod +x /app/atr-rsdwserver && \
    mkdir -p /data/serverfiles /data/logs /data/backup

# RuneScape: Dragonwilds game port (UDP). No Steam query port (discovery via EOS).
EXPOSE 7777/udp

HEALTHCHECK --interval=1m --timeout=1m --start-period=2m --retries=1 CMD /app/entrypoint-healthcheck.sh || exit 1

ENTRYPOINT ["/bin/bash", "./entrypoint.sh"]
