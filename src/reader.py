"""reader.py — чтение писем из inbox"""

from pathlib import Path
from dataclasses import dataclass

@dataclass
class Email:
    subject: str = ""
    body: str = ""

class Reader:
    # Таблица синонимов
    synonyms = {
        "from": "sender",      "от кого": "sender",   "ot kogo": "sender",
        "to": "recipient",     "кому": "recipient",   "komu": "recipient",
        "date": "date",        "дата": "date",        "data": "date",
        "subject": "subject",  "тема": "subject",     "tema": "subject",
    }

    def read_all_emails(self, inbox: Path) -> list:
        """Читаем все письма из папки и возвращаем список Email"""
        emails = []
        folder = Path(inbox)
        for file in folder.iterdir():
            emails.append(self.read_email(file))
        return emails

    def read_email(self, file: Path) -> Email:
        """Читаем письмо из файла и возвращаем словарь с заголовками и телом письма"""
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
        return Email(information.get('subject', ''), body)
        

    def _split_head_and_body(self, file: str) -> tuple:
        """Разделяем текст на заголовок и значение"""
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
        """Переводим заголовок в стандартное имя поля"""
        head = head.strip().lower()
        return self.synonyms.get(head)