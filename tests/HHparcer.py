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
        self.params = {'page': 0, 'per_page': 100}
        self.companies_data = {}

    def load_vacancies(self, companies):
        """Получает ID компании, по которому будет производится поиск по ссылке,
        циклично забирает данные по ссылке с переменной company_id и добвляет их в словарь self.vacancies"""

        for co in companies:
            company_id = co['company_id']
            response = requests.get(f"https://api.hh.ru/vacancies?employer_id={company_id}", headers=self.headers,
                                    params=self.params)
            self.vacancies = response.json()['items']
            #print(self.vacancies)
        return self.vacancies