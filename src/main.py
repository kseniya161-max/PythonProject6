from src.views import greeting_by_time, open_excel, currency_course, stock_prices, last_card_numbers
from src.services import search_trans
from src.reports import  get_expenses
import json


def main():
    file_name = "../data/trans_j.xls"
    result_2 = open_excel(file_name)

    date_str = input("Введите дату и время")
    result_1 = greeting_by_time(date_str)
    print(result_1["greeting"])


    final_result = last_card_numbers(result_2, result_1["greeting"])
    print(json.dumps(final_result, ensure_ascii=False, indent=2))

    result_3 = currency_course()
    print(result_3)

    result_4 = stock_prices()
    print(result_4)

    transactions = result_2.to_dict(orient='records')
    result_6 = search_trans(transactions)
    print(result_6)

    inp_cat = input("Введите Категорию")
    total_expenses = get_expenses(result_2, inp_cat)
    print(f"Общие траты по категории {inp_cat}: {total_expenses}")


if __name__ == "__main__":
    main()
