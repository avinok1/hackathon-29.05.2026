"""test_merge_incidents.py - файл с тестами объединителя инцидентов"""
from reader import Email
from merge_incidents import Merger
import pytest

@pytest.fixture
def merger():
    return Merger()

def test_detect_systems(merger):
    email = Email("Проблема с Confluence", "У нас полетел жестко Confluence, что делать?")
    system = merger._detect_systems(email)
    assert system == {"confluence"}

def test_email_without_system(merger):
    email = Email("Проблема с чем-то", "У нас полетел жестко что-то, что делать?")
    system = merger._detect_systems(email)
    assert system == set()

def test_similarity_same_systems(merger):
    email1 = Email("Проблема с Confluence", "У нас полетел жестко Confluence, что делать?")
    email2 = Email("Проблема с Confluence", "У нас полетел жестко Confluence, что делать?")
    assert merger._similarity(email1, email2) == 1.0

def test_similarity_different_systems(merger):
    email1 = Email("Проблема с Confluence", "У нас полетел жестко Confluence, что делать?")
    email2 = Email("Проблема с Slack", "У нас полетел жестко Slack, что делать?")
    assert merger._similarity(email1, email2) == 0.0

def test_similarity_without_systems(merger):
    email1 = Email("Проблема с чем-то", "У нас полетел жестко что-то, что делать?")
    email2 = Email("Проблема с чем-то", "У нас полетел жестко что-то, что делать?")
    assert merger._similarity(email1, email2) == 0.0

def test_group_incidents(merger):
    email1 = Email("Проблема с Confluence", "У нас полетел жестко Confluence, что делать?")
    email2 = Email("Проблема с Confluence", "У нас полетел жестко Confluence, что делать?")
    email3 = Email("Проблема с Slack", "У нас полетел жестко Slack, что делать?")
    incidents = merger.group_incidents([email1, email2, email3])
    assert len(incidents) == 2

def test_info_unknown_incident(merger):
    email = Email("Проблема с чем-то", "У нас полетел жестко что-то, что делать?", "")
    info = merger.info_one_incident([email])
    assert info["Система"] == "Неизвестная система"
    assert info["Количество писем"] == 1
    assert len(info["Отправители"]) == 1

def test_read_all_incidents_without_folder(merger, tmp_path):
    incidents = merger.read_all_incidents(tmp_path / "Папки_нет")
    assert incidents == []