import pytest
import pandas as pd
from unittest.mock import patch, mock_open
from src.views import (
    greeting_by_time,
    open_excel,
    currency_course,
    stock_prices,
    last_card_numbers
)

@pytest.mark.parametrize("input_time, expected_greeting", [
    ("2023-10-01 06:00:00", {"greeting": "Доброе Утро"}),
    ("2023-10-01 13:00:00", {"greeting": "Добрый День"}),
    ("2023-10-01 19:00:00", {"greeting": "Добрый Вечер"}),
    ("2023-10-01 00:00:00", {"greeting": "Доброй Ночи"}),
])
def test_greeting_by_time(input_time, expected_greeting):
    result = greeting_by_time(input_time)
    assert result == expected_greeting


def test_open_excel():
    mock_data = pd. DataFrame({"Категория": ["Переводы", "Фастфуд"],
                               "Сумма операции с округлением": [13500.00, 700.00]})
    with patch("pandas.read_excel", return_value=mock_data) as mock_read:
        df = open_excel("test.xlsx")
        mock_read.assert_called_once_with("test.xlsx", engine="xlrd")
        pd.testing.assert_frame_equal(df, mock_data)


@patch("os.getenv", return_value="dummy_api_key")
@patch("requests.get")
def test_currency_course(mock_get, mock_getenv):
    mock_response = {
        "conversion_rates": {
            "USD": 74.0,
            "EUR": 88.0
        }
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    expected_rates = [
        {"currency": "USD", "rate": 0.013513513513513514},
        {"currency": "EUR", "rate": 0.011363636363636364}
    ]

    result = currency_course()
    assert result == expected_rates


@patch("os.getenv", return_value="dummy_api_key")
@patch("requests.get")
def test_stock_prices(mock_get, mock_getenv):
    mock_response = {
        "Time Series (Daily)": {
            "2023-10-01": {"4. close": "150.0"},
            "2023-09-30": {"4. close": "145.0"}
        }
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    expected_data = [
        {"stock": "AAPL", "price": 150.0},
        {"stock": "AMZN", "price": 150.0},
        {"stock": "GOOGL", "price": 150.0},
        {"stock": "MSFT", "price": 150.0},
        {"stock": "TSLA", "price": 150.0},
    ]

    result = stock_prices()
    assert len(result) == 5
    for stock in expected_data:
        assert stock in result


def test_last_card_numbers():
    mock_data = pd.DataFrame({
        "Номер карты": ["1234567890123456", "2345678901234567"],
        "Сумма операции с округлением": [100.0, 200.0],
        "Дата операции": ["01.10.2023", "02.10.2023"],
        "Категория": ["Переводы", "Фастфуд"],
        "Описание": ["Описание 1", "Описание 2"]
    })

    greeting = {"greeting": "Доброе Утро"}
    result = last_card_numbers(mock_data, greeting)

    assert "cards" in result
    assert len(result["cards"]) == 2  # Две карты
    assert result["cards"][0]["last_digits"] == "3456"
    assert result["cards"][0]["total_spent"] == 100.0
    assert result["cards"][0]["cashback"] == 1.0
