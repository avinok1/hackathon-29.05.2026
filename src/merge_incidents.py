"""merge_incidents.py - файл для нахождения и объединения писем, относящихся к одному инциденту"""
from reader import Email, Reader
from pathlib import Path
from matplotlib import pyplot as p
import logging

class Merger:
    systems = ["система согласования","confluence","корпоративный портал","bi-система","облачное хранилище","slack","gitlab","service desk"]
    true_names = {
    "система согласования": "Система согласования",
    "confluence": "Confluence",
    "корпоративный портал": "Корпоративный портал",
    "bi-система": "BI-система",
    "облачное хранилище": "Облачное хранилище",
    "slack": "Slack",
    "gitlab": "GitLab",
    "service desk": "Service Desk",
}
    
    def print_info(self, incidents: list, result: str) -> None:
        """Иллюстрация информации об инцидентах"""
        incidents = sorted(incidents, key = len, reverse = True)
        names = []
        count = []
        for incident in incidents:
            info = self.info_one_incident(incident)
            names.append(info["Система"])
            count.append(info["Количество писем"])
        p.figure(figsize=(10, 5))
        p.bar(names, count)
        p.xlabel('Система')
        p.ylabel('Количество обращений')
        p.title('Инциденты по числу обращений')
        p.xticks(rotation=45, ha='right')
        p.yticks(range(0, max(count) + 1))
        p.tight_layout()
        p.savefig(result)
        logging.info(f'График инцидентов сохранен в "{result}"')

    def write_info(self, incidents: list, result: Path) -> None:
        """Записываем информацию об инцидентах в файл"""
        incidents = sorted(incidents, key = len, reverse=True)
        with open(result, 'w', encoding='utf-8') as f:
            f.write('# Отчет об инцидентах\n')
            f.write(f'Всего инцидентов: {len(incidents)}\n\n')
            for incident in incidents:
                info = self.info_one_incident(incident)
                f.write(f'## {info["Система"]}\n')
                f.write(f'- обращений: {info["Количество писем"]}\n')
                f.write(f'- количество отправителей: {len(info["Отправители"])}\n\n')
        logging.info(f'Информация об инцидентах записана в файл "{result}"')

    def info_one_incident(self, group: list) -> dict:
        """Собираем информацию об одном инциденте"""
        system = self._detect_systems(group[0])
        name = sorted(system)[0] if system else None
        truename = self.true_names.get(name, name) if system else "Неизвестная система"   
        senders = set(email.sender for email in group)
        count = len(group)
        return {"Система": truename, "Отправители": senders, "Количество писем": count}
        
    def read_all_incidents(self, folder: Path) -> list:
        """Читаем все письма из папки и возвращаем список объектов Email"""
        reader = Reader()
        emails = []
        if not folder.exists():
            logging.warning(f'Папка "{folder}" не найдена. Вероятно, инцидентов нет.')
            return emails
        for file in folder.iterdir():
            emails.append(reader.read_email(file))  
        return emails
    
    def group_incidents(self, emails: list, value: float = 0.5) -> list:
        """Группируем письма по инцидентам"""
        incidents = []  
        for email in emails:
            added = False
            for incident in incidents:
                if self._similarity(email, incident[0]) > value:
                    incident.append(email)
                    added = True
                    break
            if not added:
                incidents.append([email])
        logging.info(f'Всего инцидентов: {len(incidents)}')
        return incidents

    def _similarity(self, email1: Email, email2: Email) -> float:
        """Находим коэффициент схожести между двумя письмами и возвращаем его"""
        detected_systems1 = self._detect_systems(email1)
        detected_systems2 = self._detect_systems(email2)
        union_systems = len(detected_systems1 | detected_systems2)
        intersection_systems = len(detected_systems1 & detected_systems2)
        return intersection_systems / union_systems if union_systems > 0 else 0
    
    def _detect_systems(self, email: Email) -> set:
        """Находим системы, упомянутые в письме"""
        text = f"{email.subject} {email.body}".lower()
        detected_systems = set()
        for system in self.systems:
            if system in text:
                detected_systems.add(system)
        return detected_systems