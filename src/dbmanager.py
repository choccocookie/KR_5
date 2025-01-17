import psycopg2
from config import config
params = config()

class DBManager:

    def __init__(self, db_name, params):
        self.dbname = db_name
        self.conn = psycopg2.connect(dbname=db_name, **params)
        self.cur = self.conn.cursor()


    def get_companies_and_vacancies_count(self):
        """получает список всех компаний и количество вакансий у каждой компании"""
        query = """
                SELECT employers.employer_name, COUNT(vacancies.vacancy_id) AS vacancies_count
                FROM employers
                LEFT JOIN vacancies ON employers.employer_id = vacancies.employer
                GROUP BY employers.employer_id, employers.employer_name
                ORDER BY employers.employer_name
                """
        self.cur.execute(query)
        return {row[0]: row[1] for row in self.cur.fetchall()} #генератор словаря где row-строчка, row[0] 1 столбец строчки, row[2] 2-й столбец строчки

    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию"""
        query = """
                SELECT employers.employer_name, vacancies.vacancy_name, vacancies.salary_from, vacancies.vacancy_url
                FROM employers
                JOIN vacancies ON employers.employer_id = vacancies.employer
                """
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям, округляет до целого числа"""
        query = """
                SELECT AVG(salary_from) FROM vacancies
                """
        self.cur.execute(query)
        result = self.cur.fetchall()[0][0]
        return int(result)

    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        query = """
                SELECT * FROM vacancies
                WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies)
                """
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python"""
        query = """
                SELECT * FROM vacancies
                WHERE LOWER(vacancy_name) LIKE %s
                """
        self.cur.execute(query, ('%' + keyword.lower() + '%',))
        return self.cur.fetchall()

db=DBManager("vac", params)
#print(db.get_companies_and_vacancies_count())
#print(db.get_avg_salary())
#print(db.get_vacancies_with_higher_salary())

