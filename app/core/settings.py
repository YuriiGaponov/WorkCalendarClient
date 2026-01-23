"""
Модуль app.core.settings — конфигурация приложения WorkCalendarClient.

Определяет модель настроек приложения с валидацией через Pydantic BaseSettings.
Загружает параметры из .env‑файлов в зависимости от окружения.


Ключевые возможности:
- автоматическая загрузка переменных окружения;
- строгая валидация типов настроек;
- поддержка разных окружений (dev/test/prod) через отдельные .env‑файлы;
- приоритет переменных окружения над значениями из .env‑файлов.


Используемые компоненты:
- pydantic_settings.BaseSettings — основа для модели настроек;
- os — получение переменной окружения ENVIRONMENT;
- pathlib.Path — работа с файловыми путями;
- fastapi.templating.Jinja2Templates — инициализация шаблонов Jinja2.


Параметры окружения:
- ENVIRONMENT — режим работы (development/testing/production).
  Определяет, какой .env‑файл будет загружен.

- DATABASE_URL — строка подключения к БД (обязательный параметр).

Логика выбора файла настроек:
- значение ENVIRONMENT берётся из окружения либо по умолчанию 'development';
- подгружается файл .env.{режим} (например, .env.development);
- переменные окружения переопределяют значения из .env‑файла.

Экспортируемые объекты:
- settings — экземпляр Settings с загруженными параметрами.
  Готов к использованию в любом модуле приложения.

Требования:
- наличие соответствующего .env‑файла для выбранного окружения;
- установленный пакет pydantic-settings;
- директория data/ должна существовать либо создаваться при старте (для БД и логов);
- директория templates/ должна содержать HTML‑шаблоны.


Пример использования:
    from app.core.settings import settings
    print(settings.ENVIRONMENT)
    print(settings.DATABASE_URL)
    return templates.TemplateResponse(request, 'index.html')
"""


import os
from pathlib import Path

from fastapi.templating import Jinja2Templates
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent
"""Корневая директория проекта (подъём на 3 уровня)."""

DATA_DIR = BASE_DIR / "data"
"""Директория для данных приложения."""

ENV_MODE = os.getenv('ENVIRONMENT', 'development')
"""Режим окружения: из ENVIRONMENT или 'development' по умолчанию."""

class Settings(BaseSettings):
    """Модель настроек приложения с автоматической валидацией."""

    
    ENVIRONMENT: str = ENV_MODE
    
    DATABASE_URL: str = f"sqlite:///{DATA_DIR / 'db.sqlite3'}"

    ENCODING: str = 'utf-8'
    
    LOG_DIR: str = f"{DATA_DIR / 'log'}"
    LOG_MAX_BYTES: int = 1000000
    LOG_BACKUP_COUNT: int = 0

    TEMPLATES_DIR: str = f"{BASE_DIR / 'templates'}"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / f".env.{ENV_MODE}",
        env_file_encoding="utf-8",
        case_sensitive=False  # регистр не имеет значения для имён переменных
    )

settings = Settings()
"""
Экземпляр модели Settings с загруженными и валидированными параметрами.
Доступен для импорта в других модулях приложения.
"""
templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)
"""
Инициализированный объект Jinja2Templates для рендеринга HTML‑шаблонов.
Путь к шаблонам берётся из settings.TEMPLATES_DIR.
"""
