# OpenAI Message Processor
.
![CI/CD Pipeline](https://github.com/Gwozdziuuu/OpenAiCommunicationModule/workflows/CI/CD%20Pipeline/badge.svg)
![Docker Pulls](https://img.shields.io/docker/pulls/gwozdziuuu/openai-communication-module)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/Gwozdziuuu/OpenAiCommunicationModule)
![License](https://img.shields.io/github/license/Gwozdziuuu/OpenAiCommunicationModule)

Python application for processing text and image messages using OpenAI API. Supports both console interface and REST API with Docker deployment.

## Instalacja

```bash
pip install -r requirements.txt
```

## Użycie

### Główny punkt wejścia

```bash
# Pokaż dostępne komendy
python3 main.py help

# Aplikacja konsolowa
python3 main.py app

# Serwer REST API
python3 main.py server

# Testy
python3 main.py test

# Przykłady
python3 main.py examples
```

### Bezpośrednie uruchomienie modułów

```bash
# Aplikacja konsolowa
python3 -m src.openai_processor.app

# Serwer REST API
python3 -m src.api.server

# Testy
python3 tests/test_api.py
python3 tests/test_client.py

# Przykłady
python3 examples/basic_usage.py
```

## API Endpointy

Serwer domyślnie uruchamia się na `http://localhost:8090`

- `GET /health` - Sprawdzenie stanu serwera
- `GET /models` - Lista dostępnych modeli
- `POST /process` - Przetwarzanie wiadomości

### Przykład żądania POST /process

```json
{
  "text": "Opisz mi tę fotografię",
  "image_url": "https://example.com/image.jpg",
  "token": "sk-...",
  "model": "gpt-4o"
}
```

## Docker

### Budowanie obrazu

```bash
docker build -t openai-processor .
```

### Uruchomienie z Docker Compose

```bash
# Podstawowy serwis
docker-compose up -d

# Z nginx proxy
docker-compose --profile with-proxy up -d

# Tylko build bez uruchamiania
docker-compose build
```

### Zmienne środowiskowe

Skopiuj `.env.example` do `.env` i dostosuj:

```bash
cp .env.example .env
```

Dostępne zmienne:
- `HOST` - adres IP serwera (domyślnie: 0.0.0.0)
- `PORT` - port serwera (domyślnie: 8090) 
- `DEBUG` - tryb debugowania (domyślnie: true)
- `OPENAI_DEFAULT_MODEL` - domyślny model (domyślnie: gpt-4o)
- `OPENAI_MAX_TOKENS` - maksymalna liczba tokenów (domyślnie: 1000)
- `REQUIRE_TOKEN` - czy wymagać tokena API (domyślnie: true)
- `LOG_LEVEL` - poziom logowania (domyślnie: INFO)

### Docker Hub

Pull the latest image from Docker Hub:

```bash
# Pull and run latest version
docker pull gwozdziuuu/openai-communication-module:latest
docker run -p 8090:8090 -e OPENAI_API_TOKEN=your-token gwozdziuuu/openai-communication-module:latest

# With custom port
docker run -e PORT=3000 -p 3000:3000 gwozdziuuu/openai-communication-module:latest

# With environment file
docker run --env-file .env -p 8090:8090 gwozdziuuu/openai-communication-module:latest
```

## GitHub Repository

- **Repository**: [https://github.com/Gwozdziuuu/OpenAiCommunicationModule](https://github.com/Gwozdziuuu/OpenAiCommunicationModule)
- **Docker Hub**: [https://hub.docker.com/r/gwozdziuuu/openai-communication-module](https://hub.docker.com/r/gwozdziuuu/openai-communication-module)
- **Issues**: [Report bugs and feature requests](https://github.com/Gwozdziuuu/OpenAiCommunicationModule/issues)

## CI/CD Pipeline

The project includes automated CI/CD pipeline with GitHub Actions:

- **Continuous Integration**: Runs tests on Python 3.9
- **Docker Build**: Builds and pushes multi-platform images to Docker Hub
- **Security Scanning**: Vulnerability scanning with Trivy
- **Release Management**: Automated releases with semantic versioning

## Development

### Local Development

```bash
# Clone repository
git clone https://github.com/Gwozdziuuu/OpenAiCommunicationModule.git
cd OpenAiCommunicationModule

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your configuration

# Run locally
python main.py server
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Dependencies

- `openai>=1.0.0` - OpenAI API client
- `flask>=2.0.0` - Web framework for REST API
- `requests>=2.25.0` - HTTP testing
- `pytest>=6.0.0` - Testing framework
- `gunicorn>=20.1.0` - Production WSGI server