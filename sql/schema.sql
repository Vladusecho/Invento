-- ============================================================
-- Invento: Схема базы данных SQLite (ПР7)
-- ============================================================

-- 1. Таблица оборудования
CREATE TABLE IF NOT EXISTS equipment (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    model TEXT NOT NULL,
    serial_number TEXT NOT NULL,
    location TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'в эксплуатации'
);

-- 2. Таблица сотрудников (материально ответственных лиц)
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    email TEXT NOT NULL
);

-- 3. Таблица операций над оборудованием
CREATE TABLE IF NOT EXISTS operations (
    id INTEGER PRIMARY KEY,
    equipment_id INTEGER NOT NULL,
    employee_id INTEGER,
    operation_type TEXT NOT NULL,
    date TEXT NOT NULL,
    note TEXT NOT NULL DEFAULT '',
    is_completed INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (equipment_id) REFERENCES equipment(id),
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);
