import json
from datetime import datetime
import pandas as pd
from views import open_excel
from typing import Optional
from functools import wraps


def dec_to_file():
    """Декоратор записывает результаты функции в файл"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(str(result))
            return result
        return wrapper
    return decorator


# Декоратор с параметрами
def dec_to_file_with_param(filename: str):
    """Декоратор записывает результаты функции в указанный файл"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(filename, "w", encoding="utf-8") as f:
                f.write(str(result))
            return result
        return wrapper
    return decorator


@dec_to_file()
def get_expenses(transaction: pd.DataFrame, category: str, date_period: Optional[str] = None) -> float:
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)"""
    if date_period is None:
        date_period = datetime.now().strftime('%Y-%m-%d')
    end_date = pd.to_datetime(date_period)
    start_date = end_date - pd.DateOffset(months=3)

     # Преобразуем дату с указанием формата
    transaction["Дата платежа"] = pd.to_datetime(transaction["Дата платежа"], format='%d.%m.%Y', errors='coerce')

    # Преобразуем сумму: заменяем запятые на точки и преобразуем в float
    transaction["Сумма операции с округлением"] = transaction["Сумма операции с округлением"].astype(str).str.replace(',', '.').astype(float)
    print(transactions_df)  # Вывод всех транзакций
    print(f"Фильтр: {category}, Начало: {start_date}, Конец: {end_date}")

    filter_transactions = transaction[(transaction["Категория"] == category) &
                                          (transaction["Дата платежа"] >= start_date) &
                                          (transaction["Дата платежа"] <= end_date)
        ]
    print(filter_transactions)
    return filter_transactions["Сумма операции с округлением"].sum()


if __name__ == "__main__":
    transactions_df = open_excel('trans_j.xls')

    print(transactions_df["Категория"].unique())  # Уникальные категории
    print(transactions_df["Дата платежа"])  # Все даты

    total = get_expenses(transactions_df, "Переводы")  # Передаем категорию "Перевод"
    print(f"Общие траты по категории Переводы за последние три месяца: {total}")
    print(transactions_df["Категория"].unique())  # Уникальные категории












