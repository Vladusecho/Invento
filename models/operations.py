"""Модель операции с оборудованием (перемещение, ремонт, списание)."""

from typing import Optional

from .equipment import Equipment
from .employees import Employee


class Operation:
    """Операция над оборудованием: выдача, ремонт, списание."""

    def __init__(
        self,
        operation_id: int,
        equipment: Equipment,
        employee: Optional[Employee],
        operation_type: str,
        date: str,
        note: str = "",
    ) -> None:
        """Создать операцию.

        operation_type: 'выдача', 'возврат', 'ремонт', 'списание'
        """
        self.id = operation_id
        self.equipment = equipment
        self.employee = employee
        self.operation_type = operation_type
        self.date = date
        self.note = note
        self.is_completed = False

    def complete(self) -> None:
        """Завершить операцию."""
        self.is_completed = True

    @classmethod
    def from_data(
        cls,
        data: dict,
        equipment: Equipment,
        employee: Optional[Employee],
    ) -> "Operation":
        """Создать операцию из JSON-данных с восстановлением связей."""
        operation = cls(
            operation_id=data["id"],
            equipment=equipment,
            employee=employee,
            operation_type=data["operation_type"],
            date=data["date"],
            note=data.get("note", ""),
        )
        operation.is_completed = data.get("is_completed", False)
        return operation

    def to_data(self) -> dict:
        """Преобразовать объект в словарь для JSON (только ID связанных)."""
        return {
            "id": self.id,
            "equipment_id": self.equipment.id,
            "employee_id": self.employee.id if self.employee else None,
            "operation_type": self.operation_type,
            "date": self.date,
            "note": self.note,
            "is_completed": self.is_completed,
        }

    def __str__(self) -> str:
        """Строковое представление операции."""
        emp = self.employee.name if self.employee else "—"
        state = "завершена" if self.is_completed else "активна"
        return (
            f"[{self.id}] {self.operation_type} | "
            f"оборудование: {self.equipment.name} | "
            f"сотрудник: {emp} | дата: {self.date} | {state}"
        )