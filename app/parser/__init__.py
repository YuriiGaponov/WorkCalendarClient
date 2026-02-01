"""
Пакет WorkCalendarClient.app.parser

Предназначен для организации парсинга данных производственных календарей
из внешних источников (веб‑сайтов, API и т. п.).

Цель пакета:
- обеспечить модульную структуру для разных парсеров (по источникам данных);
- изолировать логику извлечения данных от остальной бизнес‑логики приложения;
- упростить добавление новых источников календарей.

Структура пакета:
- parser_consultant_plus.py — парсер для сайта consultant.ru;
- (в дальнейшем могут быть добавлены: parser_garant.py, parser_custom_api.py и т. д.).

Экспортируемые объекты:
- ConsultantPlusParser — класс парсера для сайта consultant.ru.
  Может быть импортирован напрямую через:
      from app.parser import ConsultantPlusParser

Использование:
    from app.parser import ConsultantPlusParser
    parser = ConsultantPlusParser(year=2025)
    calendar_data = parser.get_calendar_data()

Требования:
- наличие модуля parser_consultant_plus.py в пакете app.parser;
- установленные зависимости: requests, beautifulsoup4;
- доступ в интернет для выполнения HTTP‑запросов.

Примечания:
- Пакет спроектирован для постепенного расширения: новые парсеры добавляются как отдельные модули;
- Каждый парсер должен реализовывать унифицированный интерфейс (метод get_calendar_data);
- Рекомендуется использовать инъекции зависимостей для настройки URL/API‑ключей;
- Обработка ошибок (сеть, парсинг) должна быть локализована внутри каждого парсера.
"""

from .parser_consultant_plus import ConsultantPlusParser

__all__ = ['ConsultantPlusParser']
