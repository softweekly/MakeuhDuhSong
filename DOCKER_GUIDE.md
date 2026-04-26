# 🐳 Docker Guide for Music App

## Quick Start Commands

### Build and Run
```bash
# Build and start the container
docker-compose up --build

# Run in the background
docker-compose up -d

# Stop the container
docker-compose down
```

### Development Mode
```bash
# Run with live code reloading for development
docker-compose -f docker-compose.yml -f docker-compose.override.yml up
```

## Docker Basics for Beginners

### What is Docker?
Docker packages your application and all its dependencies into a "container" - a lightweight, portable environment that runs the same way on any machine.

### Key Docker Concepts:
- **Image**: A blueprint for creating containers
- **Container**: A running instance of an image
- **Dockerfile**: Instructions to build an image
- **docker-compose**: Tool for managing multi-container applications

## Your Music App Container Structure

```
🐳 Container Environment
├── Python 3.11 (runtime)
├── Flask web server
├── Your music app code
├── API dependencies (ElevenLabs, OpenAI)
└── Data volumes (projects persist outside container)
```

## Essential Docker Commands

### Container Management
```bash
# View running containers
docker ps

# View all containers (including stopped)
docker ps -a

# Stop a specific container
docker stop music-app

# Remove a container
docker rm music-app

# View container logs
docker logs music-app

# Execute commands inside running container
docker exec -it music-app bash
```

### Image Management
```bash
# List images
docker images

# Remove an image
docker rmi music-app

# Build image manually
docker build -t music-app .
```

### Volume Management
```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect music-app_parody_projects
```

## Production Deployment

### Environment Variables
Before deploying, ensure your `.env` file has production values:
```bash
# Copy template and edit
cp .env .env.production

# Edit with production API keys
nano .env.production
```

### Security Best Practices
1. **Never expose API keys** in Dockerfile
2. **Use non-root user** (already configured)
3. **Limit container resources**:
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '1.0'
         memory: 1G
   ```

## Scaling to Multiple Containers (Home Lab Ready)

### Phase 1: Add a Reverse Proxy (nginx)
```yaml
# Add to docker-compose.yml
nginx:
  image: nginx:alpine
  ports:
    - "80:80"
  depends_on:
    - parody-song-creator
```

### Phase 2: Add Database
```yaml
postgres:
  image: postgres:15-alpine
  environment:
    POSTGRES_DB: musicapp
    POSTGRES_USER: musicuser
    POSTGRES_PASSWORD: musicpass
  volumes:
    - postgres_data:/var/lib/postgresql/data
```

### Phase 3: Add Caching
```yaml
redis:
  image: redis:alpine
  command: redis-server --appendonly yes
  volumes:
    - redis_data:/data
```

## Home Lab Cluster Preparation

### Container Orchestration Options
1. **Docker Swarm** (easier): Built-in clustering
2. **Kubernetes** (advanced): Professional orchestration
3. **Portainer** (GUI): Web-based container management

### Docker Swarm Setup
```bash
# Initialize swarm on main node
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml musicapp
```

## Troubleshooting

### Common Issues
1. **Port already in use**: Change port in docker-compose.yml
2. **API keys not working**: Check .env file is present
3. **Container won't start**: Check logs with `docker logs music-app`

### Debug Commands
```bash
# Check container health
docker inspect music-app | grep Health

# View detailed logs
docker-compose logs -f parody-song-creator

# Enter container for debugging
docker exec -it music-app bash
```

## Monitoring and Logs

### View Real-time Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f parody-song-creator
```

### Resource Usage
```bash
# Container resource usage
docker stats

# Disk usage
docker system df
```

## Next Steps for Home Lab
1. Set up Docker on your home lab servers
2. Configure Docker Swarm or Kubernetes
3. Add monitoring (Prometheus + Grafana)
4. Set up CI/CD pipeline
5. Implement backup strategies

Happy containerizing! 🚀