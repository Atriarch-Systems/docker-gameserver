# Contributing Custom Games (Non-LGSM)

This guide explains how to add unsupported games quickly while keeping maintenance centralized.

## Design Goals

1. Preserve LinuxGSM command compatibility (`start`, `stop`, `restart`, `status`, `update`, `backup`).
2. Keep game wrappers thin and game-specific.
3. Share dependencies and security patching through one base image.

## Shared Base Image Pattern

Use [dockerfiles/Dockerfile-atr-custom-base](dockerfiles/Dockerfile-atr-custom-base) as the parent for all custom game images.

Benefits:

1. Shared dependency upgrades in one place.
2. Shared Proton update policy.
3. Lower drift between custom games.

Build and publish base first:

```powershell
$baseTag = "docker.atriarch.systems/lgsm-atr-custom-base:latest"
docker build -f dockerfiles/Dockerfile-atr-custom-base -t $baseTag .
docker push $baseTag
```

## New Custom Game Checklist

1. Add wrapper at `custom/{shortname}/{gameservername}`.
2. Add default config at `custom/{shortname}/config/_default.cfg`.
3. Add `dockerfiles/Dockerfile-{shortname}` using `FROM ${ATR_CUSTOM_BASE_IMAGE}`.
4. Register in `serverlist.csv`.
5. Build and push image (`lgsm-{shortname}`).
6. Update API requirements/catalog in the control-plane repos.
7. Validate deploy path and runtime checks in cluster.

## Wrapper Requirements

Required functions:

1. `install_server`
2. `fn_start`
3. `fn_stop`
4. `fn_status`
5. `fn_update`
6. `fn_validate`
7. `fn_backup`

Recommended hardening:

1. SteamCMD path auto-detect.
2. Runtime artifact existence checks.
3. Explicit log and pid management.

## Runtime Classification

Classify each game up front:

1. `linux-native`
2. `windows-via-proton`

For `linux-native` (e.g. RuneScape: Dragonwilds `atr-rsdw`) build directly on
the LinuxGSM base image (`FROM docker.atriarch.systems/linuxgsm:ubuntu-24.04`) —
it already ships SteamCMD, so **no** Proton/`lgsm-atr-custom-base` is required.
Add only the game's own runtime libraries (and 32-bit libs for SteamCMD), copy
the wrapper, and launch the native binary directly. This keeps the image lean
(no GE-Proton tarball).

For `windows-via-proton` include:

1. `+@sSteamCmdForcePlatformType windows` where required.
2. Proton runtime invocation.
3. First-launch telemetry checkpoints (download, verify, process handoff).

## Current Examples

1. Enshrouded: `atr-ensh` (`windows-via-proton`)
2. Space Engineers scaffold: `atr-se` (`windows-via-proton`)
3. RuneScape: Dragonwilds: `atr-rsdw` (`linux-native`)

## Release Guidance

1. Rebuild and republish `lgsm-atr-custom-base` weekly and on CVE alerts.
2. Rebuild child images after base updates.
3. Prefer pinned immutable tags or digests in deployment manifests.
