# Shared persistent BuildKit for game-server image builds

Ephemeral ARC runner pods get a **fresh, empty** BuildKit per job, so every one
of ~137 matrix builds does full network round-trips with no local layer cache.
A single long-lived `buildkitd` with a PVC-backed cache gives all jobs a warm,
shared cache and dedupes base-image pulls across parallel builds — **without any
GitHub-hosted runner or GitHub cache/storage**.

## Enable (two steps)

1. **Apply the daemon** to the same cluster the ARC runners live in:

   ```bash
   kubectl apply -f ci/buildkitd/buildkitd.yaml
   kubectl -n gh-ci rollout status deploy/buildkitd
   ```

   Set a real SSD `storageClassName` on the `buildkitd-cache` PVC first if your
   cluster has no usable default.

2. **Point the workflows at it** by setting an Actions **variable** (not secret)
   at the repo or org level:

   | Variable | Value |
   |----------|-------|
   | `BUILDKIT_REMOTE_ENDPOINT` | `tcp://buildkitd.gh-ci.svc.cluster.local:1234` |

   `build-atriarch.yml` and `build-custom.yml` each have two gated
   "Set up Docker Buildx" steps: when the variable is set they attach to this
   shared daemon (`driver: remote`); when it is empty they fall back to the
   per-job local builder. So merging the workflow change is safe **before** the
   daemon exists — it only activates once you set the variable.

## Verify

```bash
# From a runner (or any pod in-cluster):
buildctl --addr tcp://buildkitd.gh-ci.svc.cluster.local:1234 debug workers
```

A green build with the variable set, followed by a second build that reuses
layers from the first (dramatically shorter), confirms the shared cache is live.

## Notes / tuning

- **`replicas: 1` + RWO PVC** (single writer). For higher parallelism, switch to
  a horizontally-scaled BuildKit (RWX cache or per-replica PVCs) — but one warm
  daemon already removes the dominant cold-pod tax.
- Registry cache (`cache-to type=registry`) stays configured in the workflows as
  a second, cluster-independent cache tier; the two compose.
- `moby/buildkit:*-rootless` keeps the daemon unprivileged. If your cluster
  disallows the rootless `seccomp: Unconfined`, use the privileged variant per
  your security policy.
