
PS C:\Users\kapil\Desktop\Hardik\repo-intelligence> docker compose up --build
[+] up 10/10
 ✔ Image redis:7-alpine Pulled                                                                                     9.2s
[+] Building 86.4s (18/18) FINISHED
 => [internal] load local bake definitions                                                                        0.0s
 => => reading from stdin 577B                                                                                    0.0s
 => [internal] load build definition from Dockerfile                                                              0.0s
 => => transferring dockerfile: 1.40kB                                                                            0.0s 
 => [internal] load metadata for ghcr.io/astral-sh/uv:latest                                                      1.0s 
 => [internal] load metadata for docker.io/library/python:3.13-slim                                               1.6s 
 => [auth] library/python:pull token for registry-1.docker.io                                                     0.0s 
 => [internal] load .dockerignore                                                                                 0.0s
 => => transferring context: 128B                                                                                 0.0s 
 => CACHED FROM ghcr.io/astral-sh/uv:latest@sha256:a7aed3216253ee804de3e2d8afa5073baa1a177335345d43845cd4165e43b  0.0s 
 => => resolve ghcr.io/astral-sh/uv:latest@sha256:a7aed3216253ee804de3e2d8afa5073baa1a177335345d43845cd4165e43b7  0.0s 
 => [internal] load build context                                                                                 0.0s 
 => => transferring context: 8.97kB                                                                               0.0s 
 => CACHED [stage-0 1/8] FROM docker.io/library/python:3.13-slim@sha256:7c61056e61ac89e852de05f3dc6fa51a6dd21817  0.1s 
 => => resolve docker.io/library/python:3.13-slim@sha256:7c61056e61ac89e852de05f3dc6fa51a6dd2181797bceed46aa725d  0.0s 
 => [stage-0 2/8] COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/                                          0.3s
 => [stage-0 3/8] WORKDIR /app                                                                                    0.1s
 => [stage-0 4/8] RUN apt-get update     && apt-get install -y --no-install-recommends        git     && rm -rf  29.0s 
 => [stage-0 5/8] COPY pyproject.toml uv.lock ./                                                                  0.1s
 => [stage-0 6/8] RUN --mount=type=cache,target=/root/.cache/uv     uv sync --frozen --no-dev --no-install-proj  44.3s 
 => [stage-0 7/8] COPY . .                                                                                        0.1s 
 => [stage-0 8/8] RUN addgroup --system app && adduser --system --ingroup app app                                 0.4s 
 => exporting to image                                                                                            9.6s 
 => => exporting layers                                                                                           5.8s 
 => => exporting manifest sha256:b338c5fd1c58d96342a004b1ca0e523d6ccf3504e0790c90a06b2fba62efff46                 0.0s 
 => => exporting config sha256:faa4d53c7f9188b04a66a85f44296950138d1006d7f34e68a859166d22561dbf                   0.0s 
 => => exporting attestation manifest sha256:218ea6656a3fe96dd7ea9c6ebc2e8a1401d3d6f49b571b571f693bc014dc963d     0.0s 
 => => exporting manifest list sha256:812f81a2b2921eb05a0628c13982e5bc359121081d3d26a8a8c54b2c76e143e4            0.0s 
 => => naming to docker.io/library/repo-intelligence-worker:latest                                                0.0s 
[+] up 14/14king to docker.io/library/repo-intelligence-worker:latest                                             3.7s 
 ✔ Image redis:7-alpine               Pulled                                                                       9.2s
 ✔ Image repo-intelligence-worker     Built                                                                       86.7s
 ✔ Container repo-intelligence-db     Recreated                                                                    0.8s
 ✔ Container repo-intelligence-redis  Recreated                                                                    0.9s
 ✔ Container repo-intelligence-worker Recreated                                                                    1.0s
Attaching to repo-intelligence-db, repo-intelligence-redis, repo-intelligence-worker
repo-intelligence-db  |
repo-intelligence-db  | PostgreSQL Database directory appears to contain a database; Skipping initialization
repo-intelligence-db  | 
repo-intelligence-db  | 2026-09-30 18:16:43.623 UTC [1] LOG:  starting PostgreSQL 17.10 (Debian 17.10-1.pgdg12+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 12.2.0-14+deb12u1) 12.2.0, 64-bit
repo-intelligence-db  | 2026-09-30 18:16:43.624 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
repo-intelligence-db  | 2026-09-30 18:16:43.624 UTC [1] LOG:  listening on IPv6 address "::", port 5432                
repo-intelligence-db  | 2026-09-30 18:16:43.634 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"                                                                                                                    
repo-intelligence-db  | 2026-09-30 18:16:43.647 UTC [29] LOG:  database system was shut down at 2026-09-30 18:15:02 UTC
repo-intelligence-db  | 2026-09-30 18:16:43.660 UTC [1] LOG:  database system is ready to accept connections
repo-intelligence-redis  | 1:C 30 Sep 2026 18:16:43.851 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo                
repo-intelligence-redis  | 1:C 30 Sep 2026 18:16:43.851 * Redis version=7.4.11, bits=64, commit=00000000, modified=0, pid=1, just started                                                                                                     
repo-intelligence-redis  | 1:C 30 Sep 2026 18:16:43.851 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf                                                 

Container repo-intelligence-redis Waiting
repo-intelligence-redis  | 1:M 30 Sep 2026 18:16:43.851 * monotonic clock: POSIX clock_gettime
repo-intelligence-redis  | 1:M 30 Sep 2026 18:16:43.853 * Running mode=standalone, port=6379.
repo-intelligence-redis  | 1:M 30 Sep 2026 18:16:43.854 * Server initialized                                           
repo-intelligence-redis  | 1:M 30 Sep 2026 18:16:43.854 * Loading RDB produced by version 7.4.11                       
repo-intelligence-redis  | 1:M 30 Sep 2026 18:16:43.854 * RDB age 101 seconds
repo-intelligence-redis  | 1:M 30 Sep 2026 18:16:43.854 * RDB memory usage when created 1.38 Mb                        
repo-intelligence-redis  | 1:M 30 Sep 2026 18:16:43.854 * Done loading RDB, keys loaded: 6, keys expired: 1.
repo-intelligence-redis  | 1:M 30 Sep 2026 18:16:43.854 * DB loaded from disk: 0.000 seconds                           
repo-intelligence-redis  | 1:M 30 Sep 2026 18:16:43.854 * Ready to accept connections tcp                              
Container repo-intelligence-db Healthy 
Container repo-intelligence-redis Healthy 
repo-intelligence-worker  | error: Failed to initialize cache at `/nonexistent/.cache/uv`
repo-intelligence-worker  |   cause: failed to create directory `/nonexistent/.cache/uv`: Permission denied (os error 13)
repo-intelligence-worker exited with code 2 (restarting)


repo-intelligence-worker  | error: Failed to initialize cache at `/nonexistent/.cache/uv`
repo-intelligence-worker exited with code 2 (restarting)                                                               
repo-intelligence-worker  | error: Failed to initialize cache at `/nonexistent/.cache/uv`                              
repo-intelligence-worker  |   cause: failed to create directory `/nonexistent/.cache/uv`: Permission denied (os error 13)View in Docker Desktop   o View Config   w Enable Watch   d Detach
repo-intelligence-worker exited with code 2 (restarting)
repo-intelligence-worker  | error: Failed to initialize cache at `/nonexistent/.cache/uv`
repo-intelligence-worker  |   cause: failed to create directory `/nonexistent/.cache/uv`: Permission denied (os error 13)View in Docker Desktop   o View Config   w Enable Watch   d Detach
repo-intelligence-worker exited with code 2 (restarting)
repo-intelligence-worker  | error: Failed to initialize cache at `/nonexistent/.cache/uv`
repo-intelligence-worker  |   cause: failed to create directory `/nonexistent/.cache/uv`: Permission denied (os error 13)View in Docker Desktop   o View Config   w Enable Watch   d Detach
repo-intelligence-worker exited with code 2 (restarting)
repo-intelligence-worker  | error: Failed to initialize cache at `/nonexistent/.cache/uv`
repo-intelligence-worker  |   cause: failed to create directory `/nonexistent/.cache/uv`: Permission denied (os error 13)View in Docker Desktop   o View Config   w Enable Watch   d Detach
repo-intelligence-worker exited with code 2 (restarting)
repo-intelligence-worker  | error: Failed to initialize cache at `/nonexistent/.cache/uv`
repo-intelligence-worker  |   cause: failed to create directory `/nonexistent/.cache/uv`: Permission denied (os error 13)View in Docker Desktop   o View Config   w Enable Watch   d Detach
repo-intelligence-worker exited with code 2 (restarting)
repo-intelligence-worker  | error: Failed to initialize cache at `/nonexistent/.cache/uv`
repo-intelligence-worker  |   cause: failed to create directory `/nonexistent/.cache/uv`: Permission denied (os error 13)View in Docker Desktop   o View Config   w Enable Watch   d Detach
repo-intelligence-worker exited with code 2 (restarting)
repo-intelligence-worker  | error: Failed to initialize cache at `/nonexistent/.cache/uv`
repo-intelligence-worker  |   cause: failed to create directory `/nonexistent/.cache/uv`: Permission denied (os error 13)View in Docker Desktop   o View Config   w Enable Watch   d Detach
repo-intelligence-worker exited with code 2 (restarting)


v View in Docker Desktop   o View Config   w Enable Watch   d Detach# ── Stage 0: Build ────────────────────────────────────────────────────────────
FROM python:3.13-slim

# Copy the uv binary from the official image (no pip required)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Keeps Python from buffering stdout/stderr so logs appear immediately
ENV PYTHONUNBUFFERED=1 \
    # Prevent uv from downloading Python into a project-local venv
    UV_PYTHON_DOWNLOADS=never \
    # Tell uv to use the system Python
    UV_SYSTEM_PYTHON=1 \
    # Disable uv update checks inside the container
    UV_NO_PROGRESS=1 \
    # Disable uv cache — non-root system user has no writable home dir
    UV_NO_CACHE=1

WORKDIR /app

# Install system dependencies in a single layer; clean up apt cache
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first (cached unless lock/toml changes)
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

# Copy application source
COPY . .

# Create a non-root user and drop privileges
RUN addgroup --system app && adduser --system --ingroup app app
USER app

# Run the RQ worker without letting uv re-check/sync at startup
CMD ["uv", "run", "--no-sync", "rq", "worker", "ingestion"]