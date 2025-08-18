import json
import logging
import re
from typing import List, Dict
from src. services import search_trans


def test_search_trans():
    transactions = [
        {"Категории": "Переводы", "Описание": "Валерий А.", "Сумма": 1000},
        {"Категории": "Покупки", "Описание": "Роман В.", "Сумма": 500},
        {"Категории": "Переводы", "Описание": "Сергей З.", "Сумма": 500},
        {"Категории": "Покупки", "Описание": "Артем П.", "Сумма": 1500}
    ]

    expected_result = [
        {"Категории": "Переводы", "Описание": "Валерий А.", "Сумма": 1000},
        {"Категории": "Переводы", "Описание": "Сергей З.", "Сумма": 500}]



    result = search_trans(transactions)
    result_json = json.loads(result)

    assert result_json == expected_result, f"Expected {expected_result}, but got {result_json}"

