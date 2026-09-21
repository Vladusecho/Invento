"""Модель единицы оборудования."""


class Equipment:
    """Единица оборудования."""

    def __init__(
        self,
        equipment_id: int,
        name: str,
        category: str,
        model: str,
        serial_number: str,
        location: str,
        status: str = "в эксплуатации",
    ) -> None:
        """Создать объект оборудования."""
        self.id = equipment_id
        self.name = name
        self.category = category
        self.model = model
        self.serial_number = serial_number
        self.location = location
        self.status = status

    def is_in_use(self) -> bool:
        """Проверить, находится ли оборудование в эксплуатации."""
        return self.status == "в эксплуатации"

    def is_broken(self) -> bool:
        """Проверить, неисправно ли оборудование."""
        return self.status == "неисправно"

    @classmethod
    def from_data(cls, data: dict) -> "Equipment":
        """Создать оборудование из набора данных (при загрузке JSON)."""
        return cls(
            equipment_id=data["id"],
            name=data["name"],
            category=data["category"],
            model=data["model"],
            serial_number=data["serial_number"],
            location=data["location"],
            status=data.get("status", "в эксплуатации"),
        )

    def to_data(self) -> dict:
        """Преобразовать объект в словарь для JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "model": self.model,
            "serial_number": self.serial_number,
            "location": self.location,
            "status": self.status,
        }

    @staticmethod
    def validate_status(status: str) -> bool:
        """Проверить корректность статуса."""
        allowed = {"в эксплуатации", "на складе", "неисправно", "списано"}
        return status in allowed

    def __str__(self) -> str:
        """Строковое представление оборудования."""
        return (
            f"[{self.id}] {self.name} ({self.category}), "
            f"модель: {self.model}, SN: {self.serial_number}, "
            f"локация: {self.location}, состояние: {self.status}"
        )