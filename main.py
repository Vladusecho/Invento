equipment_list = []  # список словарей
next_id = 1         # автоинкремент ID


def add_equipment():
    global next_id
    name = input("Наименование: ").strip()
    category = input("Категория (ПК / Принтер / Сетевое и т.п.): ").strip()
    model = input("Модель: ").strip()
    serial = input("Серийный номер: ").strip()
    location = input("Локация: ").strip()
    status = input("Состояние (по умолчанию 'в эксплуатации'): ").strip() or "в эксплуатации"

    item = {
        "id": next_id,
        "name": name,
        "category": category,
        "model": model,
        "serial_number": serial,
        "location": location,
        "status": status,
    }
    equipment_list.append(item)
    next_id += 1
    print("Оборудование добавлено.")


def list_equipment(rows=None):
    if rows is None:
        rows = equipment_list

    if not rows:
        print("Список пуст.")
        return

    print("\n{:<4} {:<20} {:<12} {:<15} {:<15} {:<15}".format(
        "ID", "Наименование", "Категория", "Модель", "Локация", "Состояние"))
    print("-" * 95)
    for r in rows:
        print("{:<4} {:<20} {:<12} {:<15} {:<15} {:<15}".format(
            r["id"], r["name"][:19], r["category"][:11],
            r["model"][:14], r["location"][:14], r["status"][:14]))
    print()


def find_by_id(eq_id):
    for r in equipment_list:
        if r["id"] == eq_id:
            return r
    return None


def edit_equipment():
    try:
        eq_id = int(input("ID записи для редактирования: "))
    except ValueError:
        print("Введите число.")
        return

    item = find_by_id(eq_id)
    if not item:
        print("Запись не найдена.")
        return

    print("Текущие данные:", item)
    print("Поля: name, category, model, serial_number, location, status")
    field = input("Какое поле изменить? ").strip()

    if field not in item:
        print("Недопустимое поле.")
        return

    value = input("Новое значение: ").strip()
    item[field] = value
    print("Запись обновлена.")


def delete_equipment():
    try:
        eq_id = int(input("ID записи для удаления: "))
    except ValueError:
        print("Введите число.")
        return

    item = find_by_id(eq_id)
    if not item:
        print("Запись не найдена.")
        return

    confirm = input(f"Удалить '{item['name']}' (ID={eq_id})? (y/n): ").strip().lower()
    if confirm == "y":
        equipment_list.remove(item)
        print("Запись удалена.")
    else:
        print("Отменено.")


def search_equipment():
    keyword = input("Введите ключевое слово: ").strip().lower()
    result = [
        r for r in equipment_list
        if keyword in r["name"].lower()
        or keyword in r["model"].lower()
        or keyword in r["serial_number"].lower()
    ]
    list_equipment(result)


def filter_by_category():
    category = input("Введите категорию: ").strip().lower()
    result = [r for r in equipment_list if category in r["category"].lower()]
    list_equipment(result)


def menu():
    print("""
╔══════════════════════════════════════════╗
║   СИСТЕМА УЧЕТА ОБОРУДОВАНИЯ (EquipTrack)║
╠══════════════════════════════════════════╣
║ 1. Показать все                         ║
║ 2. Добавить оборудование                ║
║ 3. Редактировать оборудование           ║
║ 4. Удалить оборудование                 ║
║ 5. Поиск по названию/модели/серийнику   ║
║ 6. Фильтр по категории                  ║
║ 0. Выход                                ║
╚══════════════════════════════════════════╝
""")


def main():
    while True:
        menu()
        choice = input("Выберите пункт: ").strip()

        if choice == "1":
            list_equipment()
        elif choice == "2":
            add_equipment()
        elif choice == "3":
            edit_equipment()
        elif choice == "4":
            delete_equipment()
        elif choice == "5":
            search_equipment()
        elif choice == "6":
            filter_by_category()
        elif choice == "0":
            print("👋 Выход.")
            break
        else:
            print("❌ Неверный пункт меню.")


if __name__ == "__main__":
    main()