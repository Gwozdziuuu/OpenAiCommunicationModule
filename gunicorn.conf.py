#!/usr/bin/env python3
"""
Konfiguracja Gunicorn dla produkcji
"""

import os
from src.config import Config

# Serwer
bind = f"{Config.HOST()}:{Config.PORT()}"
workers = int(os.getenv('GUNICORN_WORKERS', '4'))
worker_class = "sync"
worker_connections = int(os.getenv('GUNICORN_WORKER_CONNECTIONS', '1000'))
timeout = int(os.getenv('GUNICORN_TIMEOUT', '30'))
keepalive = int(os.getenv('GUNICORN_KEEPALIVE', '5'))

# Logowanie
loglevel = Config.LOG_LEVEL().lower()
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'
accesslog = '-'  # stdout
errorlog = '-'   # stderr

# Proces
preload_app = True
max_requests = int(os.getenv('GUNICORN_MAX_REQUESTS', '1000'))
max_requests_jitter = int(os.getenv('GUNICORN_MAX_REQUESTS_JITTER', '100'))

# Bezpieczeństwo
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190