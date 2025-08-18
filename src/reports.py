import json
from datetime import datetime
import pandas as pd
from src.views import open_excel
from typing import Optional
from functools import wraps
import logging

# Логирование
logging.basicConfig(level=logging.INFO)


def dec_to_file():
    """Декоратор записывает результаты функции в файл"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            data_to_write = {"time": datetime.now().strftime("%Y-%m-%d_%H:%M:%S"),
                "result": result}
            # filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            logging.info("Происходит запись в файл")
            with open("response.json", "w", encoding="utf-8") as f:
                json.dump(data_to_write , f, ensure_ascii=False, indent=2)
            # with open(filename, "w", encoding="utf-8") as f:
            #     f.write(str(result))
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
    logging.info("Происходит формирование даты")
    if date_period is None:
        date_period = datetime.now().strftime('%Y-%m-%d')
    end_date = pd.to_datetime(date_period)
    start_date = end_date - pd.DateOffset(months=3)

    logging.info("Производим Преобразование даты")
    transaction["Дата платежа"] = pd.to_datetime(transaction["Дата платежа"],
                                                 format='%d.%m.%Y', errors='coerce', dayfirst=True)

    logging.info("Преобразуем сумму")
    transaction["Сумма операции с округлением"] = (transaction["Сумма операции с округлением"].
                                                   astype(str).str.replace(',', '.').astype(float))

    filter_transactions = transaction[(transaction["Категория"] == category) &
                                          (transaction["Дата платежа"] >= start_date) &
                                          (transaction["Дата платежа"] <= end_date)]
    # print(filter_transactions)
    return filter_transactions["Сумма операции с округлением"].sum()


if __name__ == "__main__":
    transactions_df = open_excel("../data/trans_j.xls")
    total = get_expenses(transactions_df, "Переводы")  # Передаем категорию "Переводы"
    print(f"Общие траты по категории Переводы за последние три месяца: {total}")
