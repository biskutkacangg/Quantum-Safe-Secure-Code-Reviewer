# ============================================================
# Dockerfile — Production-Grade Hardened Multi-Stage Build
# PQC Secure-Code Reviewer Agent
# ============================================================

# ── Stage 1: Builder ──
FROM python:3.12-slim-bookworm AS builder

WORKDIR /build

# Install system compilation dependencies securely
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies to dedicated wheels/virtualenv
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt


# ── Stage 2: Hardened Runtime ──
FROM python:3.12-slim-bookworm AS runtime

LABEL maintainer="PQC Cyber Defence Team" \
      version="1.0.0" \
      description="Production Post-Quantum Cryptography Secure-Code Reviewer Agent" \
      org.opencontainers.image.source="https://github.com/natasyafrzan-hub/Quantum-Safe-Secure-Code-Reviewer"

# Security: Install minimal runtime libraries & curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Security: Create non-root unprivileged service account
RUN groupadd -g 10001 pqcgroup && \
    useradd -u 10001 -g pqcgroup -s /sbin/nologin -d /home/pqcuser -m pqcuser

WORKDIR /app

# Copy installed Python packages from builder
COPY --from=builder --chown=pqcuser:pqcgroup /root/.local /home/pqcuser/.local

# Copy application source code
COPY --chown=pqcuser:pqcgroup . /app

# Ensure proper permissions on writable audit directory
RUN mkdir -p /app/audit_outputs && \
    chown -R pqcuser:pqcgroup /app/audit_outputs

# Security: Drop root and switch to unprivileged user
USER pqcuser
ENV PATH="/home/pqcuser/.local/bin:${PATH}" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_HEADLESS=true

# Container Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

EXPOSE 8501

# Entrypoint: Default to Web Dashboard (CLI can be invoked by passing custom args)
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
