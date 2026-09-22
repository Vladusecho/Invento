"""Тесты для класса Employee."""

import sys
from models import Employee
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def test_employee_creation():
    emp = Employee(1, "Иван Петров", "ИТ-отдел", "ivan@example.com")
    assert emp.id == 1
    assert emp.name == "Иван Петров"
    assert emp.department == "ИТ-отдел"


def test_employee_from_and_to_data():
    data = {
        "id": 1, "name": "Иван Петров",
        "department": "ИТ", "email": "ivan@example.com",
    }
    emp = Employee.from_data(data)
    assert emp.name == "Иван Петров"
    assert emp.to_data() == data


def test_employee_str():
    emp = Employee(1, "Иван Петров", "ИТ", "ivan@example.com")
    assert "Иван Петров" in str(emp)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
