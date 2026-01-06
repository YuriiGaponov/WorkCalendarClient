"""
Модуль app.core.alembic_runner.py — запуск миграций Alembic для WorkCalendarClient.

Предоставляет функцию для применения всех ожидающих миграций к базе данных
при старте приложения или в процессе развёртывания.

Назначение:
- централизованное управление применением миграций;
- автоматическая синхронизация схемы БД с моделями SQLAlchemy;
- гарантия актуальности структуры БД перед работой приложения.

Используемые компоненты:
- alembic.config.Config — загрузка конфигурации Alembic;
- alembic.command.upgrade — применение миграций до последней версии;
- engine из app.core.db — объект подключения SQLAlchemy к БД.


Функция:
- run_migrations() — загружает конфигурацию, настраивает URL БД и запускает
  миграции до версии "head" (последней).

Порядок работы:
1. Создаётся объект Config на основе файла alembic.ini.
2. В конфигурацию подставляется актуальный URL БД из engine.
3. Выполняется команда upgrade до ревизии "head".

Пример использования:
    from app.core.alembic_runner import run_migrations
    run_migrations()  # Вызвать при старте приложения

Требования:
- наличие файла alembic.ini в корне проекта;
- установленный пакет alembic;
- инициализированный engine с корректным URL подключения.

Рекомендации:
- вызывайте run_migrations() до запуска веб‑сервера;
- убедитесь, что alembic.ini содержит корректные настройки (кроме URL);
- для отладки можно добавить логирование до/после вызова функции.
"""

from alembic.config import Config
from alembic import command


def run_migrations(engine):
    """
    Применяет все ожидающие миграции Alembic к базе данных.

    Использует конфигурацию из alembic.ini и URL из SQLAlchemy engine.
    """
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", str(engine.url))
    command.upgrade(alembic_cfg, "head")
