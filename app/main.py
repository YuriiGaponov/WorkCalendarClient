"""
Модуль app.main.py — точка входа и инициализации приложения WorkCalendarClient.

Содержит основной экземпляр FastAPI, настраивает маршрутизацию и служит
стартовой точкой для запуска сервиса.

Функциональность:
- создание экземпляра приложения FastAPI;
- подключение объединённого роутера с API‑маршрутами;
- запуск миграций БД при старте;
- подготовка приложения к запуску через ASGI‑сервер.

Используемые компоненты:
- FastAPI — веб‑фреймворк для построения API;
- lifespan — контекстный менеджер для действий при старте/завершении;
- run_migrations — функция применения миграций Alembic;
- engine — объект подключения SQLAlchemy к БД;
- router — объединённый роутер со всеми API‑маршрутами.

Инициализируемые объекты:
- app — основной экземпляр FastAPI с подключёнными маршрутами.

Пример запуска через uvicorn:
    uvicorn app.main:app --host 0.0.0.0 --port 8000

Структура подключения маршрутов:
- все роутеры собираются в app.routes.__init__.py;
- в main.py подключается единый router для упрощения конфигурации.

Требования к окружению:
- установленные зависимости (fastapi, uvicorn и др.);
- настроенный Redis для кэширования (рекомендуется);
- БД PostgreSQL/SQLite (при необходимости сохранения истории).

Примечания:
- для развёртывания используйте ASGI‑серверы (uvicorn, hypercorn);
- в продакшене укажите хост и порт согласно политике безопасности;
- убедитесь, что alembic.ini доступен в корне проекта.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core import run_migrations, engine, get_logger
from app.routes import router

# main_logger = get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Менеджер жизненного цикла приложения.

    Выполняет:
    - импорт моделей для регистрации в SQLAlchemy;
    - запуск миграций Alembic при старте;
    """
    import app.models.calendar
    main_logger = get_logger()
    # Выполняется при запуске
    # print("Запуск миграций Alembic...") # заменить на logger
    main_logger.info("Запуск миграций Alembic...")
    # run_migrations()
    run_migrations(engine)
    # print("Миграции применены.") # заменить на logger
    main_logger.info("Миграции применены.")
    yield
    # Здесь можно добавить код при завершении (опционально)
    # print("Приложение завершает работу.") # заменить на logger
    main_logger.info("Приложение завершает работу.")

app = FastAPI(lifespan=lifespan)
app.include_router(router)
