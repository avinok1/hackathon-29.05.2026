"""main.py — основной файл программы"""

from reader import Reader
from distributor import Distributor

reader = Reader()
distributor = Distributor()
emails, errors = reader.read_all_emails('inbox')
distributor.distribute(emails, errors)

print(f'Всего писем: {len(emails) + len(errors)}, обработано: {len(emails)}, с ошибками: {len(errors)}')