"""Точка входа: консольное меню системы учета оборудования."""

from typing import List, Optional

from models import Equipment, Employee, Operation
from storage import (
    find_employee_by_id,
    find_equipment_by_id,
    load_employees,
    load_equipment,
    load_operations,
    save_employees,
    save_equipment,
    save_operations,
)
from utils import input_int, input_str

# ---------- Оборудование ----------

def show_equipment(equipment: List[Equipment]) -> None:
    """Вывести список оборудования."""
    if not equipment:
        print("Список оборудования пуст.")
        return
    print("\n" + "-" * 100)
    for item in equipment:
        print(item)
    print("-" * 100 + "\n")


def add_equipment(equipment: List[Equipment]) -> Equipment:
    """Добавить новую единицу оборудования."""
    new_id = max((e.id for e in equipment), default=0) + 1
    name = input_str("Наименование: ")
    category = input_str("Категория: ")
    model = input_str("Модель: ")
    serial = input_str("Серийный номер: ")
    location = input_str("Локация: ")
    status = input("Состояние (Enter — 'в эксплуатации'): ").strip() or "в эксплуатации"

    if not Equipment.validate_status(status):
        print("Недопустимый статус, установлено 'в эксплуатации'.")
        status = "в эксплуатации"

    item = Equipment(new_id, name, category, model, serial, location, status)
    equipment.append(item)
    print("Оборудование добавлено.")
    return item


def edit_equipment(equipment: List[Equipment]) -> None:
    """Редактировать запись оборудования."""
    eq_id = input_int("ID оборудования: ")
    item = find_equipment_by_id(equipment, eq_id)
    if item is None:
        print("Не найдено.")
        return

    print("Текущее:", item)
    field = input("Поле (name/category/model/serial_number/location/status): ").strip()
    if field not in {"name", "category", "model", "serial_number", "location", "status"}:
        print("Недопустимое поле.")
        return

    value = input_str("Новое значение: ")
    if field == "status" and not Equipment.validate_status(value):
        print("Недопустимый статус.")
        return

    setattr(item, field, value)
    print("Обновлено.")


def delete_equipment(equipment: List[Equipment]) -> None:
    """Удалить оборудование."""
    eq_id = input_int("ID оборудования: ")
    item = find_equipment_by_id(equipment, eq_id)
    if item is None:
        print("Не найдено.")
        return
    confirm = input(f"Удалить '{item.name}'? (y/n): ").strip().lower()
    if confirm == "y":
        equipment.remove(item)
        print("Удалено.")


def search_equipment(equipment: List[Equipment]) -> None:
    """Поиск по названию, модели, серийному номеру."""
    keyword = input_str("Ключевое слово: ").lower()
    found = [
        e for e in equipment
        if keyword in e.name.lower()
        or keyword in e.model.lower()
        or keyword in e.serial_number.lower()
    ]
    show_equipment(found)


def filter_equipment_by_category(equipment: List[Equipment]) -> None:
    """Фильтр по категории."""
    category = input_str("Категория: ").lower()
    found = [e for e in equipment if category in e.category.lower()]
    show_equipment(found)


# ---------- Сотрудники ----------

def show_employees(employees: List[Employee]) -> None:
    """Вывести сотрудников."""
    if not employees:
        print("Список сотрудников пуст.")
        return
    print("\n" + "-" * 80)
    for emp in employees:
        print(emp)
    print("-" * 80 + "\n")


def add_employee(employees: List[Employee]) -> Employee:
    """Добавить сотрудника."""
    new_id = max((e.id for e in employees), default=0) + 1
    name = input_str("ФИО: ")
    department = input_str("Отдел: ")
    email = input_str("Email: ")
    emp = Employee(new_id, name, department, email)
    employees.append(emp)
    print("Сотрудник добавлен.")
    return emp


# ---------- Операции ----------

def show_operations(operations: List[Operation]) -> None:
    """Вывести операции."""
    if not operations:
        print("Список операций пуст.")
        return
    print("\n" + "-" * 100)
    for op in operations:
        print(op)
    print("-" * 100 + "\n")


def create_operation(
    operations: List[Operation],
    equipment: List[Equipment],
    employees: List[Employee],
) -> Optional[Operation]:
    """Создать операцию: выдача / возврат / ремонт / списание."""
    eq_id = input_int("ID оборудования: ")
    eq = find_equipment_by_id(equipment, eq_id)
    if eq is None:
        print("Оборудование не найдено.")
        return None

    op_type = input_str("Тип (выдача/возврат/ремонт/списание): ").lower()
    if op_type not in {"выдача", "возврат", "ремонт", "списание"}:
        print("Недопустимый тип операции.")
        return None

    employee: Optional[Employee] = None
    if op_type == "выдача":
        emp_id = input_int("ID сотрудника: ")
        employee = find_employee_by_id(employees, emp_id)
        if employee is None:
            print("Сотрудник не найден.")
            return None

    date = input_str("Дата (YYYY-MM-DD): ")
    note = input("Примечание (Enter — пропустить): ").strip()

    new_id = max((o.id for o in operations), default=0) + 1
    op = Operation(new_id, eq, employee, op_type, date, note)

    # Изменение состояния оборудования по типу операции
    if op_type == "списание":
        eq.status = "списано"
    elif op_type == "ремонт":
        eq.status = "неисправно"
    elif op_type == "возврат":
        eq.status = "на складе"

    operations.append(op)
    print(f"Операция создана (ID={op.id}).")
    return op


def complete_operation(operations: List[Operation]) -> None:
    """Завершить операцию по ID."""
    op_id = input_int("ID операции: ")
    for op in operations:
        if op.id == op_id:
            op.complete()
            print("Операция завершена.")
            return
    print("Операция не найдена.")


# ---------- Меню ----------

def menu() -> None:
    """Показать меню."""
    print("""
╔══════════════════════════════════════════╗
║   СИСТЕМА УЧЕТА ОБОРУДОВАНИЯ (EquipTrack)║
╠══════════════════════════════════════════╣
║  ОБОРУДОВАНИЕ                            ║
║   1. Показать все                        ║
║   2. Добавить                            ║
║   3. Редактировать                       ║
║   4. Удалить                             ║
║   5. Поиск (название/модель/серийник)    ║
║   6. Фильтр по категории                 ║
║  СОТРУДНИКИ                              ║
║   7. Показать сотрудников                ║
║   8. Добавить сотрудника                 ║
║  ОПЕРАЦИИ                                ║
║   9. Показать операции                   ║
║  10. Создать операцию                    ║
║  11. Завершить операцию                  ║
║   0. Выход                               ║
╚══════════════════════════════════════════╝
""")


def main() -> None:
    """Точка входа приложения."""
    equipment = load_equipment()
    employees = load_employees()
    operations = load_operations(equipment, employees)

    print(f"Загружено: оборудование={len(equipment)}, "
          f"сотрудники={len(employees)}, операции={len(operations)}")

    while True:
        menu()
        choice = input("Выберите пункт: ").strip()

        if choice == "1":
            show_equipment(equipment)
        elif choice == "2":
            add_equipment(equipment)
        elif choice == "3":
            edit_equipment(equipment)
        elif choice == "4":
            delete_equipment(equipment)
        elif choice == "5":
            search_equipment(equipment)
        elif choice == "6":
            filter_equipment_by_category(equipment)
        elif choice == "7":
            show_employees(employees)
        elif choice == "8":
            add_employee(employees)
        elif choice == "9":
            show_operations(operations)
        elif choice == "10":
            create_operation(operations, equipment, employees)
        elif choice == "11":
            complete_operation(operations)
        elif choice == "0":
            save_equipment(equipment)
            save_employees(employees)
            save_operations(operations)
            print("Данные сохранены. Выход.")
            break
        else:
            print("Неверный пункт меню.")


if __name__ == "__main__":
    main()