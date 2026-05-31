"""test_classifier.py - файл с тестами классификатора писем"""
from reader import Email
from classifier import Classifier
import pytest
from pathlib import Path

@pytest.fixture
def classifier():
    return Classifier()

@pytest.mark.parametrize("subject, body, expected, path", [
    ('Важное письмо', 'Поздравляем, вы выиграли приз - миллион долларов!', 'Спам', 'test.txt'),
    ('Привет', 'Привет, как дела?', 'Неизвестное', 'test.txt'),
    ('Срочно', 'Срочно нужно предоставить доступ к 1С для нового сотрудника.', 'Доступы', 'test.txt'),
    ('Важное письмо', 'Поздравляем, вы выиграли - миллион долларов! Срочно прошу выдать доступ к 1С новому сотруднику.', 'Смешанная категория', 'test/test.txt'),
    ('', '', 'Неизвестное', 'test/test.txt'),
    ('ДОСТУП', 'ВЫ ПОЛУЧИЛИ ЗАРПЛАТУ! НУЖЕН РЕМОНТ ОБОРУДОВАНИЯ ПРИНТЕР НОУТБУК СКАНЕР И МЫШЬ СРОЧНО','Оборудование', 'test/test.txt'),
    ('', 'VPN ДАЙ', 'Доступы', 'test/test.txt')
])
def test_classify(classifier, subject, body, expected, path):
    path = Path(path)
    email = Email(subject, body, path)
    result = classifier.classify(email)
    assert result[0] == expected
