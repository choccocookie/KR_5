import psycopg2
from HHparcer import HH


def create_database(name, params):
    """Создание базы данных и таблиц для сохранения данных о компаниях и вакансиях."""
    try:
        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f'DROP DATABASE IF EXISTS {name}')
        cur.execute(f'CREATE DATABASE {name}')
        conn.close()

        conn = psycopg2.connect(dbname=name, **params)
        with conn.cursor() as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS employers
                        (employer_id int PRIMARY KEY,
                        employer_name varchar(100) UNIQUE NOT NULL,
                        employer_url varchar (100))
                        """)
        with conn.cursor() as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS vacancies
                        (vacancy_id int PRIMARY KEY,
                        vacancy_name varchar (100) NOT NULL,
                        vacancy_url varchar (100) NOT NULL,
                        salary_from int,
                        salary_to int,
                        employer int REFERENCES employers (varchar(100),
                        description text,
                        requirement text)
                        """)
        conn.commit()
        conn.close()

        return "База данных и таблицы успешно созданы."

    except Exception as e:
        return f"Произошла ошибка: {e}"

def insert_data(name, params):
    """Сохранение данных о компаниях и вакансиях в базу данных"""
    hh = HH()
    employers = hh.get_employers()
    vacancies = hh.get_all_vacancies()
    conn = psycopg2.connect(dbname='postgres', **params)
    with conn.cursor() as cur:
        for employer in employers:
            cur.execute(
                """
                INSERT INTO employers VALUES (%s, %s, %s)
                """, (employer["id"], employer["name"], employer["url"]))
        for vacancy in vacancies:
            cur.execute(
                """
                INSERT INTO vacancies (vacancy_id, vacancy_name, vacancy_url, salary_from, salary_to, employer, description, requirement)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s),
                """, (vacancy["id"], vacancy["name"], vacancy["url"], vacancy["salary_from"], vacancy["salary_to"],
                      vacancy["employer"], vacancy["area"], vacancy["description"], vacancy["requirement"]))
        conn.commit()
        conn.close()