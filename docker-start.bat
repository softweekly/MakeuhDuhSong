@echo off
echo 🐳 Building and starting your Music App container...

:: Check if Docker is running
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed or not running
    echo Please install Docker Desktop from https://docker.com/products/docker-desktop
    pause
    exit /b 1
)

:: Check if .env file exists
if not exist .env (
    echo ❌ .env file not found!
    echo Please make sure your .env file with API keys is present
    pause
    exit /b 1
)

:: Build and start the container
echo 📦 Building Docker image...
docker-compose build

echo 🚀 Starting Music App container...
docker-compose up -d

:: Wait a moment for container to start
timeout /t 5 /nobreak >nul

:: Check if container is running
docker-compose ps

echo ✅ Music App is starting!
echo 🌐 Open your browser and go to: http://localhost:5000
echo 
echo 📋 Useful commands:
echo   docker-compose logs -f    (view logs)
echo   docker-compose down       (stop container)
echo   docker-compose up         (start in foreground)
echo.
pause