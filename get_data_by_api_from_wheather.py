import json
import os
import requests

from dotenv import load_dotenv


load_dotenv()


def get_weather_by_api(api_key_weather, location):
    URL_WEATHER: str = "https://api.weatherapi.com/v1/current.json"
    params = {
        "key": api_key_weather,
        "q": location,
        "lang": "ru"
    }
    try:
        response = requests.get(url=URL_WEATHER, params=params)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Ошибка: сервер вернул код {response.status_code}")
    except requests.RequestException as e:
        print(f"Не удалось получить данные. Ошибка: {e}")


if __name__ == '__main__':
    kamen: str = "53.9007703,27.9766109"
    volma: str = "Volma"
    Minsk: str = "Minsk"
    data = get_weather_by_api(api_key_weather=os.getenv("API_KEY_WEATHER"), location=Minsk)

    with open("weather_today.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=True, indent=4)
