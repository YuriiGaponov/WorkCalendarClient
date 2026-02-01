"""
Модуль app.parser.parser_consultant_plus — парсер производственного календаря с сайта Consultant.ru.


Реализует извлечение данных о рабочих/выходных днях из производственного календаря
на сайте consultant.ru для заданного года.


Функционал:
- формирование URL для запроса календаря за конкретный год;
- загрузка и разбор HTML‑страницы с календарём;
- преобразование названий месяцев в числовые значения;
- извлечение номеров дней из текстовых записей;
- классификация дней по типу (рабочий, выходной, предпраздничный).


Используемые компоненты:
- requests — для выполнения HTTP‑запросов к сайту consultant.ru;
- bs4.BeautifulSoup — для парсинга HTML‑структуры страницы.


Класс:
- ConsultantPlusParser — основной класс парсера с методами для извлечения данных.


Требования:
- доступ в интернет для выполнения HTTP‑запросов;
- установленные пакеты: requests, beautifulsoup4;
- валидный год (URL должен существовать на сайте consultant.ru).


Пример использования:
    parser = ConsultantPlusParser(year=2025)
    calendar_data = parser.get_calendar_data()
    # calendar_data — список кортежей (год, месяц, день, [тип_дня])
"""

import requests
from bs4 import BeautifulSoup


class ConsultantPlusParser:
    """
    Парсер производственного календаря с сайта consultant.ru.


    Извлекает данные о рабочих, выходных и предпраздничных днях
    для заданного года из HTML‑таблиц на сайте.

    """

    MAIN_URL = 'https://www.consultant.ru/law/ref/calendar/proizvodstvennye/'
    """Базовый URL раздела производственных календарей на consultant.ru."""


    MONTH_MAPPING = {
        'январь': 1,
        'февраль': 2,
        'март': 3,
        'апрель': 4,
        'май': 5,
        'июнь': 6,
        'июль': 7,
        'август': 8,
        'сентябрь': 9,
        'октябрь': 10,
        'ноябрь': 11,
        'декабрь': 12
    }
    """Словарь для преобразования строкового названия месяца в число (1–12)."""


    def __init__(self, year: int, parser: str = 'lxml'):
        """
        Инициализирует парсер для заданного года.


        Args:
            year (int): год, для которого требуется извлечь календарь;
            parser (str): имя парсера BeautifulSoup (по умолчанию 'lxml').
        """
        self.YEAR = year
        self.parser = parser

    def _get_url(self) -> str:
        """
        Формирует URL для запроса календаря за указанный год.

        Returns:
            str: полный URL страницы календаря.
        """
        return f'{self.MAIN_URL}/{self.YEAR}/'


    def _get_response(self) -> str:
        """
        Выполняет HTTP‑запрос и возвращает HTML‑код страницы.


        Returns:
            str: текст ответа сервера (HTML).

        Raises:
            requests.RequestException: если запрос не удался (нет соединения, 404 и т. п.).
        """
        response = requests.get(self._get_url())
        response.raise_for_status()  # Поднимет исключение при ошибке HTTP
        return response.text

    def _get_soup(self) -> BeautifulSoup:
        """
        Создаёт объект BeautifulSoup для парсинга HTML.


        Returns:
            BeautifulSoup: объект для работы с DOM‑структурой страницы.
        """
        return BeautifulSoup(self._get_response(), self.parser)

    def _month_name_to_number(self, month_name: str) -> int:
        """
        Преобразует название месяца в число (1–12).


        Args:
            month_name (str): название месяца на русском (например, 'январь').


        Returns:
            int: номер месяца (1 для января, ..., 12 для декабря).


        Raises:
            ValueError: если название месяца не распознано.
        """
        normalized_name = month_name.strip().lower()
        if normalized_name not in self.MONTH_MAPPING:
            raise ValueError(f"Нераспознанное название месяца: '{month_name}'")
        return self.MONTH_MAPPING[normalized_name]


    def _get_day_number(self, day_str: str) -> int:
        """
        Извлекает числовой номер дня из текстовой записи.


        Args:
            day_str (str): строка, содержащая номер дня (может включать пробелы, символы).


        Returns:
            int: числовой номер дня (1–31).
        """
        return int(''.join(char for char in day_str if char.isdigit()))

    
    def get_calendar_data(self) -> list:
        """
        Извлекает данные календаря за указанный год.

        Проходит по всем месячным таблицам на странице, собирает информацию о днях:
        - номер года, месяца, дня;
        - тип дня (если есть: 'weekend' — выходной, 'preholiday' — предпраздничный).


        Returns:
            list: список кортежей вида:
                (год: int, месяц: int, день: int) — для рабочих дней;
                (год: int, месяц: int, день: int, тип: str) — для выходных/предпраздничных.
                Тип может быть 'weekend' или 'preholiday'.

        Пример результата:
            [
                (2025, 1, 1, 'weekend'),
                (2025, 1, 2, 'weekend'),
                ...,
                (2025, 12, 31)
            ]
        """
        result = []
        soup = self._get_soup()
        content = soup.find('div', id="content")
        month_tables = content.find_all('table', class_="cal")

        for month_table in month_tables:
            # Извлекаем название месяца и преобразуем в число
            month_th = month_table.find('th', class_="month")
            if not month_th:
                continue
            month = self._month_name_to_number(month_th.text)

            # Проходим по ячейкам дней
            day_cells = month_table.find_all('td')
            for cell in day_cells:
                class_attr = cell.get('class', [])
                # Пропускаем неактивные ячейки (например, дни другого месяца)
                if 'inactively' in class_attr:
                    continue

                day = self._get_day_number(cell.text)

                # Классифицируем день по классам
                if not class_attr:  # Нет классов — рабочий день
                    result.append((self.YEAR, month, day))
                elif 'weekend' in class_attr:
                    result.append((self.YEAR, month, day, 'weekend'))
                elif 'preholiday' in class_attr:
                    result.append((self.YEAR, month, day, 'preholiday'))

        return result
