# Задание: Создать удобную структуру для работы с курсами валют на определенную дату
# Курсы валют будем брать с этого сайта: https://www.cbr-xml-daily.ru/ .
# Нас будут интересовать только курсы доллара и евро.
# Как получить курс по API со стороннего сайта - смотри в helpers/request_currency.py

from datetime import datetime
import requests

class Currency:
    def __init__(self, currency_code: str):
        currency_code = currency_code.upper()
        if currency_code not in ('USD', 'EUR'):
            print(f"Ошибка: '{currency_code}' — неподдерживаемая валюта. Поддерживаются только 'USD' и 'EUR'")
            self.currency_code = None  # объект некорректен
        else:
            self.currency_code = currency_code

    def __getitem__(self, date_str):
        if not self.currency_code:
            return f"Объект валюты не инициализирован правильно."

        try:
            datetime.strptime(date_str, "%d.%m.%Y")
            day, month, year = date_str.split(".")
            formatted_date = year + "/" + month + "/" + day
        except ValueError:
            return f"Некорректная дата {date_str}"

        url = f"https://www.cbr-xml-daily.ru/archive/{formatted_date}/daily_json.js"
        response = requests.get(url)
        if not response.ok:
            raise ConnectionError("Ошибка при получении данных")

        date = response.json()
        try:
            return date['Valute'][self.currency_code]['Value']
        except KeyError:
            raise ValueError(f"Курс валюты {self.currency_code} не найден на дату {date_str}.")



usd = Currency("usd")  # Создаем валюту "Доллар"
euro = Currency("eur")  # Создаем валюту "Евро"
euro1 = Currency("euro")  # Создаем валюту "Евро" — неподдерживаемая валюта

print(euro1['12.10.2018'])  # ← выдаст --> Объект валюты не инициализирован правильно.
print(euro['12.14.2018'])  # ← в случае некорректной выбрасываем исключение --> Некорректная дата 12.14.2018
print(euro['07.04.2021'])   # ← получение курса евро на указанную дату
print(usd['02.09.2020'])  # ← получение курса доллара на указанную дату
