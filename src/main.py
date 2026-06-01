"""main.py — основной файл программы"""

from reader import Reader
from merge_incidents import Merger
from pathlib import Path
from distributor import Distributor
import logging
logging.basicConfig(
    filename="logs.txt",
    filemode="w",
    level=logging.INFO,
    encoding="utf-8",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

reader = Reader()
distributor = Distributor() 
emails, errors = reader.read_all_emails('inbox')
distributor.distribute(emails, errors)

print(f'Всего писем: {len(emails) + len(errors)}, обработано: {len(emails)}, писем с ошибками расширения: {len(errors)}')

merger = Merger()
incident_folder = Path('result/Инциденты')
incident_mails = merger.read_all_incidents(incident_folder)
groups = merger.group_incidents(incident_mails)
if groups:
    merger.write_info(groups, 'result/incidents.md')
    merger.print_info(groups, 'result/incidents.png')
    incidents = sorted(groups, key = len, reverse=True)
    info = merger.info_one_incident(incidents[0])
    print(f'Приоритетный инцидент: {info["Система"]}, количество обращений: {info["Количество писем"]}, количество отправителей: {len(info["Отправители"])}')
    print(f'Всего инцидентов: {len(groups)}. Информация об инцидентах записана в "result/incidents.md", график сохранен в "result/incidents.png"')
else:
    print('Инцидентов не найдено.')
    