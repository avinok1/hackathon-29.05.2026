'''reader.py — чтение писем из inbox'''

import json
from pathlib import Path
from dataclasses import dataclass
import logging

logging.basicConfig(
    filename="logs.txt",
    level=logging.INFO,
    encoding="utf-8",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

@dataclass
class Email:
    subject: str = ''
    body: str = ''

class Reader:
    # Таблица синонимов
    synonyms = {
        'from': 'sender',      'от кого': 'sender',   'ot kogo': 'sender',
        'to': 'recipient',     'кому': 'recipient',   'komu': 'recipient',
        'date': 'date',        'дата': 'date',        'data': 'date',
        'subject': 'subject',  'тема': 'subject',     'tema': 'subject',
    }

    def read_all_emails(self, inbox: Path) -> list:
        '''Читаем все письма из папки и возвращаем список писем и ошибок'''
        emails = []
        errors = []
        folder = Path(inbox)
        for file in folder.iterdir():
            logging.info (f'Происходит чтение письма "{file.name}"')
            try:
                emails.append(self.read_email(file))
                logging.info(f'Чтение письма "{file.name}" завершено')
            except Exception as e:
                errors.append((file, str(e)))
                logging.error(f'Произошла ошибка при чтении письма "{file.name}": {type(e).__name__}: {e}')
        return emails, errors
    

    def read_email(self, file: Path) -> Email:
        '''Читаем письмо из файла и возвращаем объект Email'''
        if file.suffix == '.json':
            logging.info(f'Формат файла "{file.name}": json')
            with file.open(encoding='utf-8') as f:
                letter = json.load(f)
            return Email(letter.get('subject', ''), letter.get('body', ''))
        logging.info(f'Формат файла "{file.name}": txt')
        information = {}
        with file.open(encoding='utf-8') as f:
            text = f.read()
        head, body = self._split_head_and_body(text)
        for line in head.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = self._translate_head(key)
                if key:
                    information[key] = value.strip()
        return Email(information.get('subject', ''), self._clean_body(body))
    


    def _clean_body(self, body: str) -> str:
        '''Очищаем тело письма от лишних символов и приводим к нижнему регистру'''
        marker_words = ['файл:', 'вложение:', 'во вложении:', 'прикрепил:', 'код ошибки', 'id заявки', 'p.s', 'otpravleno']
        result = []
        for line in body.lower().split('\n'):
            if any(line[:len(m)] == m for m in marker_words):
                break
            result.append(line)
        return '\n'.join(result)

    def _split_head_and_body(self, file: str) -> tuple:
        '''Разделяем текст на заголовок и значение'''
        index = 0
        file = file.split('\n')
        for line in file:
            if line == '':
                break
            index += 1
        head = '\n'.join(file[:index])
        body = '\n'.join(file[index + 1:])
        return head, body


    def _translate_head(self, head: str) -> str | None:
        '''Переводим заголовок в стандартное имя поля'''
        head = head.strip().lower()
        return self.synonyms.get(head)
