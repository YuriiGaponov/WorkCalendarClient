"""
Модуль app.core.__init__.py — инициализация пакета core WorkCalendarClient.

Обеспечивает корректную работу пакета core как компонента приложения.
Экспортирует ключевые сущности для удобного импорта в других модулях.

Назначение:
- объявляет директорию app/core Python‑пакетом;
- централизует доступ к основным объектам пакета;
- упрощает импорты (достаточно `from app.core import ...`).

Экспортируемые объекты:
- Base — декларативная база SQLAlchemy из app.core.db.
  Используется для создания моделей БД.
- engine — объект подключения SQLAlchemy к БД.
- run_migrations — функция из app.core.alembic_runner.
  Применяет миграции Alembic при старте приложения.
- settings — экземпляр настроек из app.core.settings.
  Содержит параметры конфигурации из .env‑файлов.

Пример использования:
    from app.core import Base, settings
    env = settings.ENVIRONMENT

Рекомендации:
- добавляйте в __all__ только публично доступные объекты;
- избегайте тяжёлой инициализации — файл должен загружаться быстро;
- при расширении пакета дополняйте список импортов и __all__.
"""

from .alembic_runner import run_migrations
from .db import Base, engine
from .settings import settings

__all__ = ['Base', 'engine', 'run_migrations','settings']
