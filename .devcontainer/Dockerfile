FROM python:3.12-slim

# Install Node.js 20 and other dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN python -m pip install --upgrade pip setuptools wheel

# Set working directory
WORKDIR /workspace

# Create backend virtual environment and install dependencies
COPY backend/requirements.txt ./backend/
RUN python -m venv backend/venv
RUN ./backend/venv/bin/pip install --upgrade pip setuptools wheel
RUN ./backend/venv/bin/pip install -r backend/requirements.txt

# Install frontend node dependencies
COPY frontend/package*.json ./frontend/
RUN cd frontend && npm install && cd .. || true

RUN useradd -m -s /bin/bash vscode

# Fix permissions for venv (created as root, needs to be accessible by vscode user)
RUN chown -R vscode:vscode /workspace/backend/venv

USER vscode
