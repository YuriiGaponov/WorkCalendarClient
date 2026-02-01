import requests
from bs4 import BeautifulSoup


class ConsultantPlusParser():

    MAIN_URL = 'https://www.consultant.ru/law/ref/calendar/proizvodstvennye/'

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

    def __init__(self, year: int, parser = 'lxml'):
        self.YEAR = year
        self.parser = parser
    
    def _get_url(self):
        return f'{self.MAIN_URL}/{self.YEAR}/'
    
    def _get_response(self):
        return requests.get(self._get_url()).text
    
    def _get_soup(self):
        return BeautifulSoup(self._get_response(), self.parser)
    
    def _month_name_to_number(self, month_name: str) -> int:
        normalized_name = month_name.strip().lower()
    
        if normalized_name not in self.MONTH_MAPPING:
            raise ValueError(f"Нераспознанное название месяца: '{month_name}'")
        
        return self.MONTH_MAPPING[normalized_name]
    
    def _get_data(self):
        result = []
        content = self._get_soup().find('div', id="content")
        month_tables = content.find_all('table', class_="cal")
        
        for month_table in month_tables:
            month = self._month_name_to_number(
                month_table.find('th', class_="month").text
            )
            day_tables = month_table.find_all('td')
            for day_table in day_tables:
                class_attr = day_table.get('class')
                if 'inactively' in class_attr:
                    continue
                day = day_table.text
                if len(class_attr) == 0:
                    result.append((self.YEAR, month, day))
                elif 'weekend' in class_attr:
                    result.append((self.YEAR, month, day, 'weekend'))
                elif 'preholiday' in class_attr:
                    result.append((self.YEAR, month, day, 'preholiday'))

        return result

    def get_calendar_data(self):
        print('проверка парсера')
        print(self._get_url())
        print(len(self._get_data()))
        for content in self._get_data():
            print(content)
