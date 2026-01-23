"""
Модуль app.routes.interfaces — определяет базовые маршруты API
WorkCalendarClient.

Модуль содержит роутер FastAPI с базовыми эндпоинтами. Цель —
обеспечить стартовую точку взаимодействия с приложением и заготовить
основу для расширения функциональности.


Используемые компоненты:
- FastAPI.APIRouter — механизм группировки маршрутов;
- Request (FastAPI) — объект HTTP‑запроса, передаваемый в обработчики;
- templates из `app.core` — движок шаблонов для рендеринга HTML‑страниц.


Экспортируемые объекты:
- router — экземпляр APIRouter с определёнными маршрутами.
  Может быть включён в основное приложение через
  app.include_router(router).


Определённые маршруты:
- `GET /` — эндпоинт главной страницы.
  Рендерит HTML‑шаблон `index.html` для проверки доступности сервиса.
  Предназначен для дальнейшей замены на полноценный интерфейс.


Пример подключения:
    from app.routes.interfaces import router
    app.include_router(router)


Примечания:
- Маршрут `/` возвращает `TemplateResponse` (HTML), а не текстовое сообщение.
- Модуль спроектирован для постепенного расширения: новые маршруты можно добавлять 
  в этот роутер по мере развития функционала.
- Для работы требуется настроенное окружение шаблонов (`templates`).
"""

from fastapi import APIRouter, Request

from app.core import templates


router = APIRouter()


@router.get('/')
def index_page(request: Request):
    """
    Эндпоинт главной страницы сервиса.

    Отображает HTML‑страницу `index.html` для проверки доступности сервиса.
    Предназначен для дальнейшей замены на полноценный интерфейс.

    Args:
        request (Request): Объект HTTP‑запроса от клиента.

    Returns:
        TemplateResponse: HTML‑ответ с шаблоном `index.html`.
    """
    return templates.TemplateResponse(request, 'index.html')
