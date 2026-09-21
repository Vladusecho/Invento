"""Загрузка и сохранение данных в JSON с преобразованием в объекты."""

import json
import os
from typing import List

from models import Equipment, Employee, Operation

DATA_DIR = "data"
EQUIPMENT_FILE = os.path.join(DATA_DIR, "equipment.json")
EMPLOYEES_FILE = os.path.join(DATA_DIR, "employees.json")
OPERATIONS_FILE = os.path.join(DATA_DIR, "operations.json")


def _ensure_data_dir() -> None:
    """Создать папку data, если ее нет."""
    os.makedirs(DATA_DIR, exist_ok=True)


def _load_json(path: str) -> list:
    """Загрузить JSON-файл, вернуть пустой список, если файла нет."""
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_json(path: str, data: list) -> None:
    """Сохранить данные в JSON-файл."""
    _ensure_data_dir()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_equipment() -> List[Equipment]:
    """Загрузить оборудование из JSON и преобразовать в объекты Equipment."""
    data = _load_json(EQUIPMENT_FILE)
    return [Equipment.from_data(item) for item in data]


def save_equipment(equipment: List[Equipment]) -> None:
    """Сохранить объекты Equipment в JSON."""
    _save_json(EQUIPMENT_FILE, [item.to_data() for item in equipment])


def load_employees() -> List[Employee]:
    """Загрузить сотрудников из JSON."""
    data = _load_json(EMPLOYEES_FILE)
    return [Employee.from_data(item) for item in data]


def save_employees(employees: List[Employee]) -> None:
    """Сохранить сотрудников в JSON."""
    _save_json(EMPLOYEES_FILE, [item.to_data() for item in employees])


def load_operations(
    equipment: List[Equipment],
    employees: List[Employee],
) -> List[Operation]:
    """Загрузить операции и восстановить связи с оборудованием и сотрудниками."""
    data = _load_json(OPERATIONS_FILE)
    operations: List[Operation] = []

    for item in data:
        eq = find_equipment_by_id(equipment, item["equipment_id"])
        emp = (
            find_employee_by_id(employees, item["employee_id"])
            if item.get("employee_id")
            else None
        )
        if eq is None:
            continue
        operations.append(Operation.from_data(item, eq, emp))

    return operations


def save_operations(operations: List[Operation]) -> None:
    """Сохранить операции в JSON (с ID связанных объектов)."""
    _save_json(OPERATIONS_FILE, [op.to_data() for op in operations])


# ---------- Вспомогательные функции поиска ----------

def find_equipment_by_id(
    equipment: List[Equipment], equipment_id: int
) -> Equipment | None:
    """Найти оборудование по идентификатору."""
    for item in equipment:
        if item.id == equipment_id:
            return item
    return None


def find_employee_by_id(
    employees: List[Employee], employee_id: int
) -> Employee | None:
    """Найти сотрудника по идентификатору."""
    for item in employees:
        if item.id == employee_id:
            return item
    return None