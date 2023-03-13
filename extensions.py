import requests
import json
from config import exchanges


class APIException(Exception):
    pass


class MoneyConverter:
    @staticmethod
    def get_price(base: str, sym: str, amount: str):
        if base.lower() == sym.lower():
            raise APIException(f'Невозможно перевести одинаковые валюты {base.lower()}')

        try:
            base_ticker = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {base}")

        try:
            sym_ticker = exchanges[sym.lower()]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {sym}")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать количество {amount}")

        r = requests.get(f'https://v6.exchangerate-api.com/v6/3e9735cc76c82b4e54248886/pair/{base_ticker}/{sym_ticker}')
        resp = json.loads(r.content)
        new_price = resp["conversion_rate"] * amount
        new_price = round(new_price, 3)
        message = f"Цена {amount} {base.lower()} в {sym}: {new_price}"

        return message
