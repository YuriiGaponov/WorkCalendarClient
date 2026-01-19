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
- os — получение переменной окружения ENVIRONMENT.


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
- установленный пакет pydantic-settings.


Пример использования:
    from app.core.settings import settings
    print(settings.ENVIRONMENT)
    print(settings.DATABASE_URL)
"""


import os
from pathlib import Path
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

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / f".env.{ENV_MODE}",
        env_file_encoding="utf-8",
        case_sensitive=False  # регистр не имеет значения для имён переменных
    )

settings = Settings()
