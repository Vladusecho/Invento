"""Модель сотрудника (материально ответственного лица)."""


class Employee:
    """Сотрудник организации."""

    def __init__(
        self,
        employee_id: int,
        name: str,
        department: str,
        email: str,
    ) -> None:
        """Создать объект сотрудника."""
        self.id = employee_id
        self.name = name
        self.department = department
        self.email = email

    @classmethod
    def from_data(cls, data: dict) -> "Employee":
        """Создать сотрудника из набора данных."""
        return cls(
            employee_id=data["id"],
            name=data["name"],
            department=data["department"],
            email=data["email"],
        )

    def to_data(self) -> dict:
        """Преобразовать объект в словарь для JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "department": self.department,
            "email": self.email,
        }

    def __str__(self) -> str:
        """Строковое представление сотрудника."""
        return f"[{self.id}] {self.name} ({self.department}), email: {self.email}"