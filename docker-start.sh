#!/bin/bash

echo "🐳 Building and starting your Music App container..."

# Check if Docker is running
if ! docker --version >/dev/null 2>&1; then
    echo "❌ Docker is not installed or not running"
    echo "Please install Docker from https://docker.com"
    exit 1
fi

# Check if .env file exists
if [[ ! -f .env ]]; then
    echo "❌ .env file not found!"
    echo "Please make sure your .env file with API keys is present"
    exit 1
fi

# Build and start the container
echo "📦 Building Docker image..."
docker-compose build

echo "🚀 Starting Music App container..."
docker-compose up -d

# Wait a moment for container to start
sleep 5

# Check if container is running
docker-compose ps

echo "✅ Music App is starting!"
echo "🌐 Open your browser and go to: http://localhost:5000"
echo ""
echo "📋 Useful commands:"
echo "  docker-compose logs -f    (view logs)"
echo "  docker-compose down       (stop container)"
echo "  docker-compose up         (start in foreground)"
echo ""