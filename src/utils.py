import json
import pandas as pd
from datetime import datetime


def last_card_numbers():
    # Чтение данных из Excel файла
    df = pd.read_excel("trans_j.xls", engine="xlrd")
    df.columns = df.columns.str.strip()

    # Проверка наличия необходимых столбцов
    if "Номер карты" not in df.columns or "Сумма операции с округлением" not in df.columns:
        raise ValueError("Необходимые столбцы 'Номер карты' или 'Сумма операции с округлением' не найдены в файле.")

    # print("Столбцы в DataFrame:", df.columns)

#     # Группировка данных по столбцу "from" и суммирование "amount"
    grouped = df.groupby("Номер карты")["Сумма операции с округлением"].sum().reset_index()
#
#     # Итерация по сгруппированным данным
    cards_list = []
    for index, row in grouped.iterrows():
        card_numbers = str(row["Номер карты"])[-4:]
        total = row["Сумма операции с округлением"]
        cashback = total // 100  # Кешбэк

        # print(f"По карте: {card_numbers}")
        # print(f"Общая сумма расходов: {total} рублей")
        # print(f"Кешбэк: {cashback} рублей")
        # print()  # Пустая строка для разделения записей
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

        # Формируем итоговый словарь
        result = {
            "greeting": greeting,
            "cards": cards_list,
            "top_transactions": transactions_list
        }
        return result

if __name__ == "__main__":
    date_input = "2023-10-01 14:30:00"
    greeting = greeting_by_time(date_input)  # Получаем приветствие

    # Открываем Excel файл
    df = open_excel("trans_j.xls")

    # Получаем итоговый результат
    final_result = last_card_numbers(df)

    # Преобразуем в JSON-строку
    json_response = json.dumps(final_result, ensure_ascii=False, indent=2)  # Добавляем отступы для удобства чтения
    print(json_response)  # Вывод JSON-строки

    # Сохранение JSON в файл
    with open("response.json", "w", encoding="utf-8") as f:
        json.dump(final_result, f, ensure_ascii=False, indent=2)  # Записываем словарь в файл



