# ── Stage 0: Build ────────────────────────────────────────────────────────────
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
    UV_NO_PROGRESS=1

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