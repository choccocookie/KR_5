import psycopg2
from dbmanager import DBManager
from src.utils import create_database, create_tables, insert_data
from hhparcer import HH
from config import config

params = config()
create_database("c_work", params)
create_tables("c_work", params)
insert_data("c_work", params)

def main():
    db_manager = DBManager("c_work", params)
    while True:
        print(f'Выберите запрос: \n'
              f'1 - Список всех компаний и количество вакансий у каждой компании\n'
              f'2 - Cписок всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на '
              f'вакансию\n'
              f'3 - Средняя зарплата по вакансиям\n'
              f'4 - Список всех вакансий, у которых зарплата выше средней по всем вакансиям\n'
              f'5 - Список всех вакансий, в названии которых содержатся запрашиваемое слово\n'
              f'6 - Выход\n')
        user_request = input()
        if user_request == '1':
            companies_vacancies_count = db_manager.get_companies_and_vacancies_count()
            print(f"Список всех компаний и количество вакансий у каждой компании:\n {companies_vacancies_count}")
        elif user_request == '2':
            vacancy_list = db_manager.get_all_vacancies()
            print(f"Cписок всех вакансий с указанием названия компании, вакансии, зарплаты и ссылки на вакансию:\n "
                  f"{vacancy_list}")
        elif user_request == '3':
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплату по вакансиям:\n {avg_salary}")
        elif user_request == '4':
            vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
            print(f"Список всех вакансий, у которых зарплата выше средней по всем вакансиям:\n "
                  f"{vacancies_with_higher_salary}")
        elif user_request == '5':
            user_input = input(f'Введите слово: ')
            vacancies_with_keyword = db_manager.get_vacancies_with_keyword(user_input)
            print(f"список всех вакансий, в названии которых содержатся\n {user_input}: {vacancies_with_keyword}")
        elif user_request == '6':
            break
        else:
            print(f"Введён неверный запрос")

if __name__ == "__main__":
    main()
