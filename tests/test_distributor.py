"""test_distributor.py - файл с тестами распределителя файлов по категориям"""

from reader import Email
from distributor import Distributor
import pytest
from pathlib import Path

@pytest.fixture
def distributor():
    return Distributor()

def test_move_corrent_and_incorrect_files(tmp_path, monkeypatch, distributor):
    monkeypatch.chdir(tmp_path)
    correct_file = tmp_path / 'correct.txt'
    correct_file.write_text('Subject: Срочно\nBody: Нужно предоставить доступ')
    incorrect_file = tmp_path / 'incorrect.bin'
    incorrect_file.write_text('Привет! Как дела?')
    errors =[(incorrect_file, 'json.decoder.JSONDecodeError')]
    distributor.distribute([Email('Срочно', 'Нужно предоставить доступ', correct_file)], errors)
    assert (tmp_path / 'result/Доступы/correct.txt').exists()
    assert (tmp_path / 'result/errors/incorrect.bin').exists()