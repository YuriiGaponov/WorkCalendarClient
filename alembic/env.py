"""
Модуль alembic.env.py — конфигурация Alembic для WorkCalendarClient.

Определяет логику выполнения миграций БД:
- подключение к SQLAlchemy engine из приложения;
- настройку контекста Alembic;
- обработку режимов offline/online.

Назначение:
- синхронизация схемы БД с моделями SQLAlchemy через миграции;
- поддержка генерации миграций (autogenerate);
- обеспечение корректного подключения к БД при выполнении миграций.

Используемые компоненты:
- SQLAlchemy — ORM и движок подключения;
- Alembic — система миграций;

Ключевые объекты:
- target_metadata — метаданные моделей из app.core.db.Base;
- engine — готовое подключение к БД из приложения;
- context — контекст Alembic с настройками из alembic.ini.

Режимы выполнения:
- offline — генерация SQL‑скриптов без подключения к БД;
- online — прямое применение миграций к БД.

Требования:
- установленный пакет alembic;
- корректный файл alembic.ini в корне проекта;
- инициализированный SQLAlchemy engine с валидным URL подключения.

Рекомендации:
- не редактируйте этот файл при стандартной работе с миграциями;
- для генерации миграций используйте `alembic revision --autogenerate`;
- проверяйте сгенерированные миграции вручную перед применением в продакшене.
"""

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from app.core.db import Base, engine
import app.models # Импорт всех моделей для БД до нанлиза метаданных Base


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
