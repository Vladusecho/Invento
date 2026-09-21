"""Тесты для класса Equipment."""

from models import Equipment


def test_equipment_creation():
    eq = Equipment(1, "Ноутбук Dell", "ПК", "Latitude 5420", "SN-001", "Аудитория 305")
    assert eq.id == 1
    assert eq.name == "Ноутбук Dell"
    assert eq.category == "ПК"
    assert eq.status == "в эксплуатации"


def test_equipment_is_in_use():
    eq = Equipment(1, "Ноутбук", "ПК", "M1", "SN1", "305")
    assert eq.is_in_use()
    eq.status = "списано"
    assert not eq.is_in_use()
    assert not eq.is_broken()


def test_equipment_from_and_to_data():
    data = {
        "id": 1, "name": "Принтер HP", "category": "Принтер",
        "model": "LJ1102", "serial_number": "HP-1",
        "location": "Склад", "status": "на складе",
    }
    eq = Equipment.from_data(data)
    assert eq.name == "Принтер HP"
    assert eq.to_data() == data


def test_equipment_validate_status():
    assert Equipment.validate_status("в эксплуатации")
    assert Equipment.validate_status("списано")
    assert not Equipment.validate_status("нечто")


def test_equipment_str():
    eq = Equipment(1, "Ноутбук", "ПК", "M1", "SN1", "305")
    text = str(eq)
    assert "Ноутбук" in text
    assert "SN1" in text