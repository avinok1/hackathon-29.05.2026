"""main.py — основной файл программы"""

from reader import Reader
from distributor import Distributor
import logging
logging.basicConfig(
    filename="logs.txt",
    filemode="w"
    level=logging.INFO,
    encoding="utf-8",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

reader = Reader()
distributor = Distributor()
emails, errors = reader.read_all_emails('inbox')
distributor.distribute(emails, errors)

print(f'Всего писем: {len(emails) + len(errors)}, обработано: {len(emails)}, с ошибками: {len(errors)}')