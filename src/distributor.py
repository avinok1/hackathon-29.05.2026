"""distributor.py — распределение писем по папкам категорий"""

from classifier import Classifier
from dataclasses import dataclass
from pathlib import Path
import logging


class Distributor:
    def distribute(self, emails, errors):
        '''Распределяем письма по папке категории'''
        classifier = Classifier()
        result_way = Path('result')
        for email in emails:
            category, file = classifier.classify(email)
            category_folder = result_way / category
            category_folder.mkdir(parents=True, exist_ok=True)
            file.rename(category_folder / file.name)
            logging.info(f'файл {file.name} теперь в папке {category_folder}')
    

        for file, error in errors:
            error_folder = result_way / 'errors'
            error_folder.mkdir(parents=True, exist_ok=True)
            file.rename(error_folder / file.name)
            logging.error(f'файл {file.name} теперь в папке errors, причина = {error}')
