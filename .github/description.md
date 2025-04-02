# OpenMCP Workspace

A comprehensive Contextual Memory Manager dashboard designed for AI workspaces, with a planned evolution path towards Web4 decentralization.

## 🚀 Overview

OpenMCP Workspace is a monorepo containing multiple applications and libraries for managing contextual memory in AI environments. The project is designed to be modular, scalable, and future-proof, with a clear path towards Web4 decentralization.

## 🏗️ Architecture

The project consists of four main components:

1. **Dashboard (Frontend)**
   - React-based web interface
   - TypeScript for type safety
   - Material-UI for components
   - Real-time updates via WebSocket

2. **Backend API**
   - FastAPI-based REST service
   - PostgreSQL for structured data
   - S3 for large object storage
   - JWT authentication

3. **MCP Server**
   - JSON-RPC endpoint
   - Context routing and management
   - LLM integration
   - Storage abstraction layer

4. **Shared Libraries**
   - AWS integration
   - LLM adapter
   - Monitoring client
   - Utility functions

## 📊 Current Status

- **Test Coverage**: 23% overall
  - Libraries: 23% (15 tests)
  - Dashboard: 19.29%
  - Backend: In progress
  - MCP Server: In progress

- **Features Implemented**:
  - ✅ Basic dashboard UI
  - ✅ Backend API endpoints
  - ✅ AWS S3 integration
  - ✅ LLM text generation
  - ✅ Monitoring metrics
  - ✅ Database migrations

- **In Progress**:
  - 🔄 Test coverage improvement
  - 🔄 Error handling
  - 🔄 Logging system
  - 🔄 Documentation

## 🛠️ Tech Stack

### Frontend
- React 18
- TypeScript
- Vite
- Material-UI
- Vitest for testing

### Backend
- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL
- pytest

### Infrastructure
- Docker
- Docker Compose
- Prometheus
- Grafana
- AWS S3

## 🚦 Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/openmcp-workspace.git
   cd openmcp-workspace
   ```

2. Set up environment:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. Start services:
   ```bash
   docker-compose -f docker-compose.dev.yml up -d
   ```

4. Run applications:
   ```bash
   # Backend
   cd apps/backend
   uvicorn src.main:app --reload --port 8000

   # Dashboard
   cd apps/dashboard
   npm run dev
   ```

## 📝 Documentation

- [Architecture Overview](docs/architecture.md)
- [API Documentation](docs/api.md)
- [Development Guide](docs/development.md)
- [Upgrade Plan](docs/upgrade_plan.md)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔮 Future Roadmap

1. **Short Term**
   - Improve test coverage
   - Add error handling
   - Enhance logging
   - Complete documentation

2. **Medium Term**
   - Add more LLM providers
   - Implement caching
   - Add performance monitoring
   - Enhance security features

3. **Long Term**
   - Web4 integration
   - IPFS storage
   - Smart contract support
   - Cross-chain capabilities

## 📞 Support

- Create an issue for bug reports
- Join our community discussions
- Check our documentation
- Contact the maintainers

## 🙏 Acknowledgments

- FastAPI team for the excellent framework
- React team for the frontend library
- All contributors and maintainers 