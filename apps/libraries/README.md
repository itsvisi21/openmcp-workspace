# OpenMCP Libraries

A collection of libraries for the OpenMCP project.

## Project Status

### Current Status
- ✅ Core library functionality implemented
  - ✅ AWS S3 client with upload, download, and delete operations
  - ✅ LLM client with text generation and embedding capabilities
  - ✅ Monitoring client with metric and event recording
  - ✅ Utility functions for configuration management and data processing
- ✅ Test framework set up with pytest and coverage reporting
  - ✅ 15 test cases implemented
  - ✅ Coverage reporting configured
  - ✅ Async test support with pytest-asyncio
- ✅ Environment configuration and dependency management
  - ✅ Python 3.11+ compatibility
  - ✅ Dependency version management
  - ✅ Environment variable configuration
- ✅ Documentation and examples
  - ✅ API documentation
  - ✅ Usage examples
  - ✅ Environment setup guide

### Test Coverage (23% overall)
- ✅ `library.py`: 100% coverage
  - ✅ Configuration merging
  - ✅ JSON parsing
  - ✅ Dictionary operations
- ⚠️ `aws/client.py`: 0% coverage
  - ⚠️ S3 upload functionality
  - ⚠️ S3 download functionality
  - ⚠️ S3 delete functionality
- ⚠️ `llm/client.py`: 0% coverage
  - ⚠️ Text generation
  - ⚠️ Text embedding
  - ⚠️ Model configuration
- ⚠️ `monitoring/client.py`: 0% coverage
  - ⚠️ Metric recording
  - ⚠️ Event recording
  - ⚠️ Prometheus integration
- ⚠️ `__init__.py` files: 0% coverage
  - ⚠️ Package initialization
  - ⚠️ Module exports

### Implementation Status
1. AWS Integration
   - ✅ Basic S3 operations
   - ⚠️ Error handling
   - ⚠️ Retry mechanisms
   - ⚠️ Batch operations

2. LLM Integration
   - ✅ Basic text generation
   - ✅ Text embedding
   - ⚠️ Model parameter tuning
   - ⚠️ Response streaming

3. Monitoring Integration
   - ✅ Basic metric recording
   - ✅ Event recording
   - ⚠️ Custom metric types
   - ⚠️ Alert configuration

### Feature Backlog
1. High Priority
   - [ ] Implement comprehensive tests for AWS client
   - [ ] Implement comprehensive tests for LLM client
   - [ ] Implement comprehensive tests for Monitoring client
   - [ ] Add error handling and retry mechanisms
   - [ ] Add logging and debugging capabilities

2. Medium Priority
   - [ ] Add type hints and documentation
   - [ ] Implement caching mechanisms
   - [ ] Add performance monitoring
   - [ ] Add integration tests
   - [ ] Add CI/CD pipeline

3. Low Priority
   - [ ] Add more AWS service integrations
   - [ ] Add more LLM provider support
   - [ ] Add more monitoring metrics
   - [ ] Add benchmarking tools
   - [ ] Add development tools and scripts

## Installation

```bash
pip install -e ".[test]"  # Install with test dependencies
```

## Available Libraries

### AWS Library
AWS integration library for OpenMCP.

```python
from openmcp.aws import S3Client

client = S3Client()
await client.upload_file("file.txt", "bucket", "key")
```

### LLM Library
LLM integration library for OpenMCP.

```python
from openmcp.llm import LLMClient

client = LLMClient()
response = await client.generate("Hello, world!")
```

### Monitoring Library
Monitoring library for OpenMCP.

```python
from openmcp.monitoring import MonitoringClient

client = MonitoringClient()
await client.record_metric("request_count", 1)
```

## Development

### Running Tests

```bash
# Run tests with coverage
pytest --cov=src --cov-report=term-missing

# Run tests without coverage
pytest
```

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# AWS Settings
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=us-east-1
AWS_BUCKET_NAME=your-bucket

# LLM Settings
LLM_PROVIDER=openai
LLM_MODEL=gpt-4
LLM_MAX_TOKENS=2000
LLM_TEMPERATURE=0.7

# Monitoring Settings
ENABLE_MONITORING=true
MONITORING_INTERVAL=60
PROMETHEUS_MULTIPROC_DIR=./prometheus_data
SENTRY_DSN=your-sentry-dsn
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and ensure coverage
5. Submit a pull request

## License

MIT License 