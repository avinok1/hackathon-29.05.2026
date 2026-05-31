"""merge_incidents.py - файл для нахождения и объединения писем, относящихся к одному инциденту"""
from reader import Email, Reader
from pathlib import Path
from matplotlib import pyplot as p

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
            names.append(self.true_names.get(list(info["Система"])[0], list(info["Система"])[0]))
            count.append(info["Количество писем"])
        p.figure(figsize=(10, 5))
        p.bar(names, count)
        p.xlabel('Система')
        p.ylabel('Количество обращений')
        p.title('Инцеденты по числу обращений')
        p.xticks(rotation=45, ha='right')
        p.tight_layout()
        p.savefig(result)

    def write_info(self, incidents: list, result: Path) -> None:
        """Записываем информацию об инцидентах в файл"""
        incidents = sorted(incidents, key = len, reverse=True)
        with open(result, 'w', encoding='utf-8') as f:
            f.write('# Отчет об инцидентах\n')
            f.write(f'Всего инцидентов: {len(incidents)}\n\n')
            for incident in incidents:
                info = self.info_one_incident(incident)
                f.write(f'## {self.true_names.get(list(info["Система"])[0], list(info["Система"])[0])}\n')
                f.write(f'- обращений: {info["Количество писем"]}\n')
                f.write(f'- количество отправителей: {len(info["Отправители"])}\n\n')

    def info_one_incident(self, group: list) -> dict:
        """Собираем информацию об одном инциденте"""
        system = self._detect_systems(group[0])
        senders = set(email.sender for email in group)
        count = len(group)
        return {"Система": system, "Отправители": senders, "Количество писем": count}
        
    def read_all_incidents(self, folder: Path) -> list:
        """Читаем все письма из папки и возвращаем список объектов Email"""
        reader = Reader()
        emails = []
        for file in folder.iterdir():
            emails.append(reader.read_email(file))
        return emails
    
    def group_incidents(self, emails: list, value: float = 0.3) -> list:
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