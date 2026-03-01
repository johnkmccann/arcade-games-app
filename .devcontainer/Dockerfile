FROM python:3.12-slim

# Install dependencies and Node.js 20 with explicit repository setup
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    ca-certificates \
    gnupg \
    && mkdir -p /usr/share/keyrings \
    && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource.gpg.key | gpg --dearmor -o /usr/share/keyrings/nodesource.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list \
    && apt-get update \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace

# Copy build requirements
COPY .devcontainer/requirements.txt ./

# Upgrade pip, setuptools, and wheel using pinned versions
RUN pip install -r requirements.txt

# Create backend virtual environment and install dependencies
COPY backend/requirements.txt ./backend/
RUN python -m venv backend/venv
RUN ./backend/venv/bin/pip install -r requirements.txt
RUN ./backend/venv/bin/pip install -r backend/requirements.txt

# Install frontend node dependencies
COPY frontend/package*.json ./frontend/
RUN cd frontend && npm install

RUN useradd -m -s /bin/bash vscode

# Fix permissions for venv and node_modules (created as root, needs to be accessible by vscode user)
RUN chown -R vscode:vscode /workspace/backend/venv
RUN chown -R vscode:vscode /workspace/frontend/node_modules

USER vscode
