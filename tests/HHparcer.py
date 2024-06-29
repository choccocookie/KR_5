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