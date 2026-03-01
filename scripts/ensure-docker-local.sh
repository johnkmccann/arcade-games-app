#!/bin/bash

# Local Docker startup script for macOS
# Run this locally before opening the dev container

echo "🍎 Checking Docker Desktop..."

# Check if docker CLI is installed
if ! command -v docker &> /dev/null; then
  echo "❌ Docker CLI is not installed or not in your PATH."
  echo "📥 Please install Docker Desktop from: https://www.docker.com/products/docker-desktop"
  exit 1
fi

# Check if Docker is running
if ! docker ps > /dev/null 2>&1; then
  echo "⚠️  Docker Desktop is not running. Starting it now..."
  open -a Docker
  
  # Wait for Docker to be ready
  echo "Waiting for Docker Desktop to start..."
  for i in {1..60}; do
    if docker ps > /dev/null 2>&1; then
      echo "✅ Docker Desktop is ready!"
      exit 0
    fi
    echo -n "."
    sleep 1
  done
  
  echo ""
  echo "❌ Docker Desktop took too long to start. Opening it manually may help."
  exit 1
else
  echo "✅ Docker Desktop is already running!"
  exit 0
fi
