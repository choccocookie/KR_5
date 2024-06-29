#import config
import requests
import json
from abc import ABC, abstractmethod
#from vacanсy import Vacancy

class Parser(ABC):
    """
    Абстрактный класс для работы с API
    """


    @abstractmethod
    def load_vacancies(self):
        pass



class HH(Parser):
    """
    Класс для работы с API HeadHunter

    """

    def __init__(self):
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'page': 0, 'per_page': 10, 'sort_by': 'by_vacancies_open'}
        self.companies_data = {
            'Тиньков': 78638,
            'Яндекс': 1740,
            'Билайн': 4934,
            'Сбербанк': 1473866,
            'Банк ВТБ': 4181,
            'Газпромнефть': 39305,
            'Альфа-банк': 80,
            'СберТех': 3529,
            'ФинТех IQ': 5898393,
            'Айтеко': 872178
        }

    def __get_requests(self):
        """
        :return: возвращает список открытых вакансий
        """
        response = requests.get('https://api.hh.ru/employers', params=self.params)
        if response.status_code == 200:
            return response.json()['items']

    def get_employers(self):
        """
        Проходит по списку вакансий и делает выборку id, name, url работодателей
        :return:
        """
        employers = []
        data = self.__get_requests()
        for employer in data:
            employers.append({"id": employer["id"], "name": employer["name"], "url": employer["url"]})
        return employers

    def get_companies(self):
        """
            Получает имя компаний и их ID,
            :return: список словарей с информацией о компаниях
            """
        companies = []

        for company_name, company_id in self.companies_data.items():
            company_url = f"https://hh.ru/employer/{company_id}"
            company_info = {'company_id': company_id, 'company_name': company_name, 'company_url': company_url}
            companies.append(company_info)
        return companies

    def __get_vacancies_on_employer(self, id):
        """
        :param id: id компании, параметр взят из документации к API HH
        :return: список вакансий указанной компании
        """
        params = {"employer_id": id}
        response = requests.get("https://api.hh.ru/vacancies", params=params)
        if response.status_code == 200:
            return response.json()["items"]

    def get_all_vacancies(self):
        """
        через метод self.get_employers() получает список организаций, берет id организации
        и передает в метод self.__get_vacancies_on_employer, который формирует список вакансий организации
        в соответствии с выбранными ключами
        """
        employers = self.get_employers()
        all_vacancies = []
        for employer in employers:
            vacancies = self.__get_vacancies_on_employer(employer["id"])
            for vacancy in vacancies:
                if vacancy["salary"] is None:
                    salary_from = 0
                    salary_to = 0
                else:
                    salary_from = vacancy["salary"]["from"] if vacancy["salary"]["from"] else 0
                    salary_to = vacancy["salary"]["to"] if vacancy["salary"]["to"] else 0
                all_vacancies.append({"id": vacancy["id"], "name": vacancy["name"],
                                      "url": vacancy["alternate_url"],
                                      "salary_from": salary_from,
                                      "salary_to": salary_to,
                                      "employer": employer["id"],
                                      "area":vacancy["area"]["name"]})
        return all_vacancies

    def load_vacancies(self, companies):
        """Получает ID компании, по которому будет производится поиск по ссылке,
        циклично забирает данные по ссылке с переменной company_id и добвляет их в словарь self.vacancies"""

        for co in companies:
            company_id = co['company_id']
            response = requests.get(f"https://api.hh.ru/vacancies?employer_id={company_id}", headers=self.headers,
                                    params=self.params)
            self.vacancies = response.json()['items']
        return self.vacancies


hh = HH()
print(hh.get_employers())