"""test_classifier.py - файл с тестами классификатора писем"""
from reader import Email
from classifier import Classifier
import pytest

@pytest.fixture
def classifier():
    return Classifier()

@pytest.mark.parametrize("subject, body, expected", [
    ('Важное письмо', 'Поздравляем, вы выиграли приз - миллион долларов!', 'Спам'),
    ('Привет', 'Привет, как дела?', 'Неизвестное'),
    ('Срочно', 'Срочно нужно предоставить доступ к 1С для нового сотрудника.', 'Доступы'),
    ('Важное письмо', 'Поздравляем, вы выиграли - миллион долларов! Срочно прошу выдать доступ к 1С новому сотруднику.', 'Смешанная категория'),
    ('', '', 'Неизвестное'),
    ('ДОСТУП', 'ВЫ ПОЛУЧИЛИ ЗАРПЛАТУ! НУЖЕН РЕМОНТ ОБОРУДОВАНИЯ ПРИНТЕР НОУТБУК СКАНЕР И МЫШЬ СРОЧНО','Оборудование'),
    ('', 'VPN ДАЙ', 'Доступы')
])
def test_classify(classifier, subject, body, expected):
    email = Email(subject, body)
    result = classifier.classify(email)
    assert result[0] == expected
