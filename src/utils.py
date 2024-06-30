import psycopg2


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
            cur.execute(f'CREATE TABLE IF NOT EXISTS employers '
                        f'(employer_id int PRIMARY KEY, '
                        f'employer_name varchar(100) UNIQUE NOT NULL, '
                        f'employer_url varchar (100))')
        with conn.cursor() as cur:
            cur.execute(f'CREATE TABLE IF NOT EXISTS vacancies '
                        f'(vacancy_id int PRIMARY KEY, '
                        f'vacancy_name varchar (100) NOT NULL,'
                        f'vacancy_url varchar (100) NOT NULL'
                        f'salary_from int,'
                        f'salary_to int,'
                        f'employer int REFERENCES employers (varchar(100),'
                        f'salary_from int, '
                        f'salary_to int,'
                        f'description text,'
                        f'requirement text)')
        conn.commit()
        conn.close()

        return "База данных и таблицы успешно созданы."

    except Exception as e:
        return f"Произошла ошибка: {e}"