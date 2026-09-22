"""Тесты для класса Operation."""

from models import Equipment, Employee, Operation


def _make_equipment() -> Equipment:
    return Equipment(1, "Ноутбук", "ПК", "M1", "SN1", "305")


def _make_employee() -> Employee:
    return Employee(1, "Иван", "ИТ", "ivan@example.com")


def test_operation_creation():
    eq = _make_equipment()
    emp = _make_employee()
    op = Operation(1, eq, emp, "выдача", "2026-09-15")
    assert op.id == 1
    assert op.equipment is eq
    assert op.employee is emp
    assert op.operation_type == "выдача"
    assert not op.is_completed


def test_operation_complete():
    op = Operation(1, _make_equipment(), _make_employee(), "ремонт", "2026-09-15")
    op.complete()
    assert op.is_completed


def test_operation_to_data():
    eq = _make_equipment()
    emp = _make_employee()
    op = Operation(1, eq, emp, "выдача", "2026-09-15")
    data = op.to_data()
    assert data["equipment_id"] == 1
    assert data["employee_id"] == 1
    assert data["operation_type"] == "выдача"


def test_operation_from_data():
    eq = _make_equipment()
    emp = _make_employee()
    data = {
        "id": 1, "equipment_id": 1, "employee_id": 1,
        "operation_type": "выдача", "date": "2026-09-15",
        "note": "", "is_completed": False,
    }
    op = Operation.from_data(data, eq, emp)
    assert op.equipment is eq
    assert op.employee is emp
    assert op.operation_type == "выдача"
