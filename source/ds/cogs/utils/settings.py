"""
Файл для удобства настроек бота со всеми необходимыми переменными
"""
import logging  # PyCharm ругается что импорт не нужен, хотя это не так
from pathlib import Path
from logging.config import dictConfig
from discord import Object
from .secret.discord_keys import GUILD, DEV

# Базовая директория бота
BASE_DIR = Path(__file__).parents[2]

# Директория наборов команд
COGS_DIR = BASE_DIR / 'cogs'

# ID сервера разработчика
DEV_GUILD_ID = Object(id=int(GUILD))

# ID разработчика
DEV_ID = Object(id=int(DEV))

# Настройки для логирования
LOGGING_CONFIG = {
    'version': 1,
    'disabled_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(levelname)s - %(module)s : %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/info.log',
            'mode': 'w',
            'formatter': 'standard'
        }
    },
    'loggers': {
        'bot': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        },
        'discord': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False
        }
    }
}

dictConfig(LOGGING_CONFIG)
