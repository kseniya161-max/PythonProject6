import json
from datetime import datetime


# def greeting_by_time():
#     """ Программа приветствует в соответствии с текущим временем суток"""
#     #создаем объект datetime
#     dt = datetime.now()
#
#     if 5 <= dt.hour < 12:
#         greeting = "Доброе Утро"
#     elif 12 <= dt.hour < 18:
#         greeting = "Добрый День"
#     elif 18 <= dt.hour < 24:
#         greeting = "Добрый Вечер"
#     else:
#         greeting = "Доброй Ночи"
#
#         # Формируется json файл
#     response = {"greeting": greeting}
#     return json.dumps(response, ensure_ascii=False)
#
# if __name__ == "__main__":
#     print(greeting_by_time())


def greeting_by_time(date_str):
    """ Программа приветствует в соответствии с переданным временем суток"""
    # создаем объект datetime из строки
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

    if 5 <= dt.hour < 12:
        greeting = "Доброе Утро"
    elif 12 <= dt.hour < 18:
        greeting = "Добрый День"
    elif 18 <= dt.hour < 24:
        greeting = "Добрый Вечер"
    else:
        greeting = "Доброй Ночи"

    # Формируется json файл
    response = {"greeting": greeting}
    return response

if __name__ == "__main__":
    date_input = "2023-10-01 14:30:00"
    response = greeting_by_time(date_input)  # Получаем словарь
    json_response = json.dumps(response, ensure_ascii=False)  # Преобразуем в JSON-строку
    print(json_response)  # Вывод JSON-строки

    # Сохранение JSON в файл
    with open("response.json", "w", encoding="utf-8") as f:
        json.dump(response, f, ensure_ascii=False)  # Записываем словарь в файл