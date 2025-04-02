# OpenMCP Workspace

A Contextual Memory Manager dashboard designed for AI workspaces, with a planned evolution path towards Web4 decentralization.

## Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- Docker and Docker Compose
- Git

## Development Environment Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/openmcp-workspace.git
cd openmcp-workspace
```

### 2. Environment Setup

```bash
# Copy environment variables template
cp .env.example .env

# Edit .env with your settings
# Required variables:
# - AWS credentials and settings
# - LLM provider settings
# - Database credentials
# - Monitoring settings
```

### 3. Start Development Services

```bash
# Start required services (PostgreSQL, Prometheus, Grafana)
docker-compose -f docker-compose.dev.yml up -d

# Verify services are running
docker-compose -f docker-compose.dev.yml ps
```

### 4. Backend Setup

```bash
# Navigate to backend directory
cd apps/backend

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -e ".[dev]"

# Run database migrations
alembic upgrade head

# Start the development server
uvicorn src.main:app --reload --port 8000
```

### 5. MCP Server Setup

```bash
# Navigate to MCP server directory
cd apps/mcp-server

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -e ".[dev]"

# Start the development server
uvicorn src.main:app --reload --port 8001
```

### 6. Libraries Setup

```bash
# Navigate to libraries directory
cd apps/libraries

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest --cov=src --cov-report=term-missing
```

### 7. Dashboard Setup

```bash
# Navigate to dashboard directory
cd apps/dashboard

# Install dependencies
npm install

# Start the development server
npm run dev

# Run tests
npm run test
npm run coverage
```

## Development Workflow

### Running Tests

```bash
# Backend tests
cd apps/backend
pytest

# MCP Server tests
cd apps/mcp-server
pytest

# Libraries tests
cd apps/libraries
pytest

# Dashboard tests
cd apps/dashboard
npm run test
```

### Code Style

- Python: Follow PEP 8 guidelines
- TypeScript: Follow ESLint configuration
- Use pre-commit hooks for consistent formatting

### Git Workflow

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit:
   ```bash
   git add .
   git commit -m "feat: your feature description"
   ```

3. Push changes:
   ```bash
   git push origin feature/your-feature-name
   ```

4. Create a pull request

## Monitoring and Debugging

### Accessing Services

- Backend API: http://localhost:8000
- MCP Server: http://localhost:8001
- Dashboard: http://localhost:5173
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

### Logs

```bash
# View all service logs
docker-compose -f docker-compose.dev.yml logs -f

# View specific service logs
docker-compose -f docker-compose.dev.yml logs -f service_name
```

## Troubleshooting

### Common Issues

1. **Port Conflicts**
   - Check if ports 8000, 8001, 5173, 9090, or 3000 are in use
   - Modify ports in docker-compose.dev.yml if needed

2. **Database Connection**
   - Verify PostgreSQL is running: `docker-compose -f docker-compose.dev.yml ps`
   - Check database credentials in .env
   - Run migrations if needed: `alembic upgrade head`

3. **Test Failures**
   - Ensure all services are running
   - Check environment variables
   - Run tests with verbose output: `pytest -v`

## Project Structure

```
openmcp-workspace/
├── apps/
│   ├── backend/          # FastAPI backend service
│   ├── mcp-server/       # MCP server implementation
│   ├── dashboard/        # React dashboard
│   └── libraries/        # Shared Python libraries
├── docs/                 # Project documentation
├── docker/              # Docker configuration
├── environments/        # Environment configurations
└── scripts/            # Utility scripts
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and ensure coverage
5. Submit a pull request

## License

MIT License 