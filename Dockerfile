# Użyj oficjalnego obrazu Python
FROM python:3.11-slim

# Ustaw zmienne środowiskowe
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

# Ustaw katalog roboczy
WORKDIR /app

# Skopiuj i zainstaluj zależności
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj kod aplikacji
COPY . .

# Utwórz użytkownika bez uprawnień administratora
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port (domyślny 8090)
EXPOSE ${PORT:-8090}

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8090}/health || exit 1

# Domyślne komendy
# Rozwój: CMD ["python3", "main.py", "server"]
# Produkcja: 
CMD ["gunicorn", "--config", "gunicorn.conf.py", "src.api.server:create_app()"]