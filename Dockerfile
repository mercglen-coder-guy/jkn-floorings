# ==========================================
# STAGE 1: Builder (Install Dependencies)
# ==========================================
FROM python:3.12-slim AS builder

# Prevent python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /build

# Install build dependencies (if any are compiled)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment for isolated dependency packaging
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy dependency configs
COPY requirements.txt .

# Install dependencies (without dev caches to keep size tiny)
RUN pip install --no-cache-dir -r requirements.txt

# ==========================================
# STAGE 2: Production Runtime
# ==========================================
FROM python:3.12-slim AS runner

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"

# Create a non-privileged user and group for maximum container security
RUN groupadd -g 10001 litestar && \
    useradd -u 10001 -g litestar -s /bin/sh -m litestar

WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy application directories with correct owner permissions
COPY --chown=litestar:litestar Home.py .
COPY --chown=litestar:litestar Templates/ Templates/
COPY --chown=litestar:litestar static/ static/

# Switch to the non-root user for security
USER litestar

# Expose production port
EXPOSE 8080

# Launch server
CMD ["uvicorn", "Home:app", "--host", "0.0.0.0", "--port", "8080"]
