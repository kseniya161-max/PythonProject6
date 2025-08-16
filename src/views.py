import json
import pandas as pd
from datetime import datetime
import requests
import os
from dotenv import load_dotenv
import logging


#Логирование
logging.basicConfig(level=logging.INFO)

def greeting_by_time(date_str):
    """ Программа приветствует в соответствии с переданным временем суток"""
    logging.info("Создается объект datetime из строки")
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

    if 5 <= dt.hour < 12:
        greeting = "Доброе Утро"
    elif 12 <= dt.hour < 18:
        greeting = "Добрый День"
    elif 18 <= dt.hour < 24:
        greeting = "Добрый Вечер"
    else:
        greeting = "Доброй Ночи"

    # Формируется json ответ
    response = {"greeting": greeting}
    return response


def open_excel(file_name):
    """ Открываем Excel и загружаем его в DataFrame """
    logging.info("Производится открытие Exel файла")
    df = pd.read_excel(file_name, engine="xlrd")
    return df


def currency_course():
    """ Функция получает актуальный курс валют"""
    load_dotenv()  # Загружает переменные окружения из файла .env
    logging.info("Производится запрос на Api сайт")
    api_key = os.getenv("API_KEY")  # Получает значение переменной окружения
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/RUB"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        rates = data["conversion_rates"]

        currency_rates = [
            {"currency": "USD", "rate": 1 / rates.get("USD", None)},
            {"currency": "EUR", "rate": 1 / rates.get("EUR", None)}]

        return currency_rates
    else:
        print("Ошибка при получении данных о курсах валют.")
        return []


def stock_prices():
    """ Функция получает цены акций S&P 500"""
    load_dotenv()
    api_key = os.getenv("API_KEY_ALPHA_VANTAGE")
    tickers = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]  # Пример тикеров
    stock_data = []
    for ticker in tickers:

        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}"
        response = requests.get(url)
        logging.info("Получаем данные с API сайта")
        if response.status_code == 200:
            data = response.json()
            if "Time Series (Daily)" in data:
                latest_date = list(data["Time Series (Daily)"].keys())[0]
                latest_data = data["Time Series (Daily)"][latest_date]
                stock_data.append({
                    "stock": ticker,
                    "price": float(latest_data["4. close"])
                })
            else:
                print(f"Ошибка получения данных для {ticker}: {data}")
        else:
            print(f"Ошибка API для {ticker}: {response.status_code}")
    return stock_data


def last_card_numbers(df,greeting):
    # Чтение данных из Excel файла
    df.columns = df.columns.str.strip()

    logging.info("Происходит проверка наличия необходимых столбцов")
    if "Номер карты" not in df.columns or "Сумма операции с округлением" not in df.columns:
        raise ValueError("Необходимые столбцы 'Номер карты' или 'Сумма операции с округлением' не найдены в файле.")


    logging.info("Происходит группировка данных по столбцам")
    grouped = df.groupby("Номер карты")["Сумма операции с округлением"].sum().reset_index()

   # Итерация по сгруппированным данным
    cards_list = []
    for index, row in grouped.iterrows():
        card_numbers = str(row["Номер карты"])[-4:]
        total = row["Сумма операции с округлением"]
        cashback = total // 100  # Кешбэк

        cards_list.append({
            "last_digits": card_numbers,
            "total_spent": total,
            "cashback": cashback
        })

    # Преобразовывем столбец в Экселе "Дата платежа" в df
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], errors='coerce', dayfirst=True)
    # Получение 5 транзакций
    top_transactions = df.nlargest(5, "Сумма операции с округлением")
    transactions_list = []
    for index, row in top_transactions.iterrows():
        transactions = {"date": row["Дата операции"]. strftime("%d.%m.%Y"),
                        "amount": row["Сумма операции с округлением"],
                        "category": row["Категория"],
                        "description": row["Описание"]

        }
        transactions_list.append(transactions)
    currency_rates = currency_course()

    logging.info("Формируем итоговой словарь")
    result = {
            "greeting": greeting,
            "cards": cards_list,
            "top_transactions": transactions_list,
            "currency_rates": currency_rates,
            "stock_prices": stock_prices()
    }
    return result


if __name__ == "__main__":
    date_input = "2023-10-01 14:30:00"
    logging.info("Выводится приветствие")
    greeting = greeting_by_time(date_input)

    # Открываем Excel файл
    df = open_excel("../data/trans_j.xls")
    file_name = "../data/trans_j.xls"

    # Получаем итоговый результат
    final_result = last_card_numbers(df, greeting)
    final_result["currency_rates"] = currency_course()
    final_result["stock_prices"] = stock_prices()

    # Преобразуем в JSON-строку
    json_response = json.dumps(final_result, ensure_ascii=False, indent=2)
    print(json_response)  # Вывод JSON-строки

    # Сохранение JSON в файл
    with open("response.json", "w", encoding="utf-8") as f:
        json.dump(final_result, f, ensure_ascii=False, indent=2)  # Записываем в json

