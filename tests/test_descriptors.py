import sys
import pytest 
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src_lab2')))

from class_task import Task


def test_empty():
    task = Task("1", "valid description")
    assert task.description == "valid description"


def test_empty_string():
    with pytest.raises(ValueError):
        Task("1", "")


def test_non_string():
    with pytest.raises(TypeError):
        Task("1", 123)


def test_reading():
    task = Task("1", "desc")
    assert task.id == "1"


def test_reading_change():
    task = Task("1", "desc")
    with pytest.raises(AttributeError):
        task.id = "2"


def test_choice():
    task = Task("1", "desc", priority="high")
    assert task.priority == "high"


def test_priority():
    task = Task("1", "desc")
    with pytest.raises(ValueError):
        task.priority = "urgent"


def test_status():
    task = Task("1", "desc", status="new")
    assert task.status == "new"


def test_invalid_status():
    task = Task("1", "desc")
    with pytest.raises(ValueError):
        task.status = "wrong"


def test_description():
    task = Task("1", "  text  ")
    assert task.description == "  text  "


def test_id():
    with pytest.raises(ValueError):
        Task("", "desc")