import json
import pandas as pd


# def last_card_numbers():
#     # Чтение данных из Excel файла
#     df = pd.read_excel("operations.xlsx", engine="openpyxl")

#     df.columns = df.columns.str.strip()
#
#     # Проверка наличия необходимых столбцов
#     if "Номер карты" not in df.columns or "Сумма операции" not in df.columns:
#         raise ValueError("Необходимые столбцы 'Номер карты' или 'Сумма операции' не найдены в файле.")
#
#     print("Столбцы в DataFrame:", df.columns)
#
# #     # Группировка данных по столбцу "from" и суммирование "amount"
#     grouped = df.groupby("Номер карты")["Сумма операции"].sum().reset_index()
# #
# #     # Итерация по сгруппированным данным
#     for index, row in grouped.iterrows():  # Исправлено: заменено на 'for index, row in grouped.iterrows()'
#         card_numbers = str(row["Номер карты"])[-4:]  # Исправлено: 'row' вместо 'index.row'
#         total = row["Сумма операции"]
#         cashback = total // 100  # Кешбэк (1 рубль на каждые 100 рублей)
#
#         print(f"По карте: {card_numbers}")
#         print(f"Общая сумма расходов: {total} рублей")
#         print(f"Кешбэк: {cashback} рублей")
#         print()  # Пустая строка для разделения записей
#
# last_card_numbers()


def last_card_numbers():
    # Чтение данных из Excel файла
    df = pd.read_excel("trans_j.xls", engine="xlrd")

    df.columns = df.columns.str.strip()

    # Проверка наличия необходимых столбцов
    if "Номер карты" not in df.columns or "Сумма операции с округлением" not in df.columns:
        raise ValueError("Необходимые столбцы 'Номер карты' или 'Сумма операции с округлением' не найдены в файле.")

    print("Столбцы в DataFrame:", df.columns)

#     # Группировка данных по столбцу "from" и суммирование "amount"
    grouped = df.groupby("Номер карты")["Сумма операции с округлением"].sum().reset_index()
#
#     # Итерация по сгруппированным данным
    for index, row in grouped.iterrows():
        card_numbers = str(row["Номер карты"])[-4:]
        total = row["Сумма операции с округлением"]
        cashback = total // 100  # Кешбэк

        print(f"По карте: {card_numbers}")
        print(f"Общая сумма расходов: {total} рублей")
        print(f"Кешбэк: {cashback} рублей")
        print()  # Пустая строка для разделения записей

    top_transactions = df.nlargest(5, "Сумма операции с округлением")
    for index, row in top_transactions.iterrows():
        print(f"Номер карта: {row["Номер карты"]}, Сумма: {row["Сумма операции с округлением"]} рублей")


last_card_numbers()
