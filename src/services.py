import json
import logging
import re
from typing import List, Dict


# логирование
logging.basicConfig(level=logging.INFO)


def search_trans(transactions: List[Dict]) -> str:
    """ Функция ищет переводы по физическим лицам """
    logging.info("Начало поиска")
    filtered_transactions = []
    pattern = re.compile(r"^[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.$")
    """ Проверяем есть ли категории переводы"""
    logging.info("Происходит поиск по фильтру: Переводы в Категории")
    for trans in transactions:
        if trans.get("Категории") == "Переводы" and pattern.search(trans.get("Описание", "")):
            filtered_transactions.append(trans)

    logging.info(f"Найдено {len(filtered_transactions)} переводов физическим лицам")
    return json.dumps(filtered_transactions, ensure_ascii=False)


if __name__ == "__main__":
    transactions = [
        {"Категории": "Переводы", "Описание": "Валерий А.", "Сумма": 1000},
        {"Категории": "Покупки", "Описание": "Роман В.", "Сумма": 500},
        {"Категории": "Переводы", "Описание": "Сергей З.", "Сумма": 500},
        {"Категории": "Покупки", "Описание": "Артем П.", "Сумма": 1500}
    ]

    result = search_trans(transactions)
    print(result)
