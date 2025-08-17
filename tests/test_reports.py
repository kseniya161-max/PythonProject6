import pandas as pd
import pytest
from src.reports import get_expenses, dec_to_file
from src.views import open_excel
import os
from unittest.mock import mock_open, patch
from src.reports import dec_to_file_with_param



@pytest.fixture
def data_ex():
    data = {
        "Дата платежа": ["31.07.2025", "16.07.2025", "20.07.2025"],
        "Категория": ["Переводы", "Фастфуд", "Супермаркеты"],
        "Сумма операции с округлением": ["219,00", "700,00", "244,90"]
    }
    return pd.DataFrame(data)


def test_get_expenses(data_ex):
    "Тестируем на актуальный вывод"
    total = get_expenses(data_ex, "Переводы", "2025-07-31")
    assert total == 219.00


def test_period(data_ex):
    "Тестируем если выводим дату за пределами"
    total = get_expenses(data_ex, "Переводы", "2026-07-31")
    assert total == 0.0

def test_get_expenses_no_category(data_ex):
    "Тестируем если выводим неизвестную категорию"
    total = get_expenses(data_ex, "Неизвестная категория", "2025-07-31")
    assert total == 0.0


@dec_to_file_with_param("test_output.json")
def my_func(value):
    return {"result": f"Категории: {value}"}

def test_dec_to_file_with_param():
    mock = mock_open()
    with patch("builtins.open", mock):
        result = my_func("Переводы")

    assert result == {"result": "Категории: Переводы"}







