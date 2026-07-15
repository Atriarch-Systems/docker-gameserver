#
# Atriarch Custom Game Runtime Base Image
#
# Shared base for non-LGSM-supported custom games using SteamCMD + Proton.
# Child images should only add game-specific wrapper scripts and defaults.
#

# Base image is pulled from the Atriarch Nexus registry, not Docker Hub, to
# avoid WAN/rate-limits and keep all pulls on-registry.
ARG LGSM_BASE_IMAGE=docker.atriarch.systems/linuxgsm:ubuntu-24.04
FROM ${LGSM_BASE_IMAGE}

LABEL maintainer.fork="Atriarch Systems <postmaster@mail.atriarch.systems>"
LABEL image.role="atr-custom-base"
ARG GE_PROTON_VERSION=10-26
# Optional integrity check; when set, the downloaded tarball must match.
ARG GE_PROTON_SHA256=""

ENV PROTON_ROOT=/opt/proton
ENV PROTON_PATH=/opt/proton/GE-Proton${GE_PROTON_VERSION}/proton
ENV STEAM_COMPAT_CLIENT_INSTALL_PATH=/usr/lib/games/steam

WORKDIR /app

RUN dpkg --add-architecture i386 && \
                apt-get update && \
                apt-get install --no-install-recommends -y \
            ca-certificates \
            curl \
            dbus \
                        fontconfig \
                        fonts-liberation \
            jq \
            lib32gcc-s1 \
                        libfontconfig1:i386 \
            libfreetype6 \
                        libfreetype6:i386 \
            python3 \
                        xauth \
                        xvfb \
            winbind && \
        rm -rf /var/lib/apt/lists/*

# GE-Proton is pulled from the Atriarch CDN first (fast, on-net, no GitHub rate
# limit), falling back to the upstream GitHub release if the CDN copy is absent.
# Optional GE_PROTON_SHA256 enforces integrity when provided.
RUN set -eux && \
    mkdir -p ${PROTON_ROOT} && \
    tarball="/tmp/GE-Proton${GE_PROTON_VERSION}.tar.gz" && \
    ( curl -fsSL -o "${tarball}" "https://cdn.atriarch.systems/proton/GE-Proton${GE_PROTON_VERSION}.tar.gz" || \
      curl -fsSL -o "${tarball}" "https://github.com/GloriousEggroll/proton-ge-custom/releases/download/GE-Proton${GE_PROTON_VERSION}/GE-Proton${GE_PROTON_VERSION}.tar.gz" ) && \
    if [ -n "${GE_PROTON_SHA256}" ]; then echo "${GE_PROTON_SHA256}  ${tarball}" | sha256sum -c -; fi && \
    tar -xzf "${tarball}" -C ${PROTON_ROOT} && \
    rm -f "${tarball}"

# Child images will set game-specific GAMESERVER and STEAM_COMPAT_DATA_PATH.

ENTRYPOINT ["/bin/bash", "./entrypoint.sh"]
