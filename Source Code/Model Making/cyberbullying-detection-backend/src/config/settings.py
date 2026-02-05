import os
from datetime import timedelta
import logging.config

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
    CORS_HEADERS = 'Content-Type'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    MODEL_NAME = "nlptown/bert-base-multilingual-uncased-sentiment"
    DEBUG = True
    
    # Redis configuration for rate limiting
    RATELIMIT_STORAGE_URL = "redis://localhost:6379"
    RATELIMIT_STORAGE_OPTIONS = {}
    RATELIMIT_KEY_PREFIX = "limiter"

    # Logging configuration
    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'default': {
                'level': 'INFO',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
            },
            'file': {
                'level': 'INFO',
                'formatter': 'standard',
                'class': 'logging.FileHandler',
                'filename': 'app.log',
                'mode': 'a',
            },
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['default', 'file'],
                'level': 'INFO',
                'propagate': True
            }
        }
    }