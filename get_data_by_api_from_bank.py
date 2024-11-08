import json
import datetime

import requests

today = datetime.date.today()


def get_curses_today_by_api() -> dict:
    """
    Возвращает словарь курсов USD, EUR, RUB, CNY.
    """
    api_url = 'https://api.nbrb.by/exrates/rates/'
    curses = {
        "USD": f"{api_url}USD?parammode=2",
        "EUR": f"{api_url}EUR?parammode=2",
        "RUB": f"{api_url}RUB?parammode=2",
        "CNY": f"{api_url}CNY?parammode=2"
    }

    curses_today = {}

    for key, url_api in curses.items():
        try:
            response = requests.get(url=url_api)
            if response.status_code == 200:
                data = response.json()
                curses_today[key] = f"{data['Cur_OfficialRate']}"
            else:
                print(f"Ошибка: для {key} сервер вернул код {response.status_code}")
        except requests.RequestException as e:
            print(f"Не удалось получить данные для {key}: {e}")

    return curses_today


if __name__ == '__main__':
    data_curses = get_curses_today_by_api()
    print(data_curses)

    # with open("cur_day.json", "w", encoding="utf-8") as file:
    #     json.dump(curses_today, file, indent=4, ensure_ascii=True)
    #
    # with open("cur_day.json", "r", encoding="utf-8") as file:
    #     data = json.load(file)
    #     print(type(data))
    #     for k, v in data.items():
    #         print(k, v)
