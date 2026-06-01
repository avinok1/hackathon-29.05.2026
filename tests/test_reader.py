"""test_reader.py - файл с тестами чтения писем"""
from reader import Reader
import pytest
import json

@pytest.fixture
def reader():
    return Reader()

def test_read_broken_json_file(reader, tmp_path):
    file = tmp_path / "hi.json"
    file.write_text("{subject: 'Привет', body: 'Как дела?'", encoding="utf-8")
    with pytest.raises(json.decoder.JSONDecodeError):
        reader.read_email(file)

def test_read_empty_file(reader, tmp_path):
    file = tmp_path / "empty.txt"
    file.write_text("", encoding="utf-8")
    email = reader.read_email(file)
    assert email.subject == ""
    assert email.body == ""

def test_read_correct_json_file(reader, tmp_path):
    file = tmp_path / "email.json"
    file.write_text('{"subject": "Привет", "body": "Как дела?", "from": "test@example.com"}', encoding="utf-8")
    email = reader.read_email(file)
    assert email.subject == "Привет"
    assert email.body == "Как дела?"
    assert email.sender == "test@example.com"
    
def test_both_correct_and_incorrect_files(reader, tmp_path):
    correct_file = tmp_path / "correct.txt"
    correct_file.write_text("From: test@example.com\nSubject: Привет\n\nКак дела?", encoding="utf-8")
    incorrect_file = tmp_path / "incorrect.json"
    incorrect_file.write_text("{subject: 'Привет', body: 'Как дела?'", encoding="utf-8")
    emails, errors = reader.read_all_emails(tmp_path)
    assert emails[0].subject == "Привет"
    assert emails[0].body == "как дела?"
    assert emails[0].sender == "test@example.com"
    assert len(errors) == 1

