"""
Модуль app.core.settings — конфигурация приложения WorkCalendarClient.

Определяет модель настроек приложения с валидацией через Pydantic BaseSettings.
Загружает параметры из .env‑файлов в зависимости от окружения.

Ключевые возможности:
- автоматическая загрузка переменных окружения;
- валидация типов настроек;
- поддержка разных окружений (dev/test/prod) через отдельные .env‑файлы.

Используемые компоненты:
- pydantic_settings.BaseSettings — основа для модели настроек;
- os — получение переменной окружения ENVIRONMENT.

Параметры окружения:
- ENVIRONMENT — режим работы (development/testing/production).
  Определяет, какой .env‑файл будет загружен.

Логика выбора файла настроек:
- значение ENVIRONMENT берётся из окружения либо по умолчанию 'development';
- подгружается файл .env.{режим} (например, .env.development).

Экспортируемые объекты:
- settings — экземпляр Settings с загруженными параметрами.
  Готов к использованию в любом модуле приложения.

Требования:
- наличие соответствующего .env‑файла для выбранного окружения;
- установленный пакет pydantic-settings.

Пример использования:
    from app.core.settings import settings
    print(settings.ENVIRONMENT)
"""

import os

from pydantic_settings import BaseSettings

env_mode = os.getenv('ENVIRONMENT', 'development')

class Settings(BaseSettings):
    """Модель настроек приложения с автоматической валидацией."""

    ENVIRONMENT: str = env_mode

    class Config:
        env_file = f".env.{env_mode}"
        env_file_encoding = "utf-8"

settings = Settings()
