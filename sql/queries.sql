-- ============================================================
-- Invento: Набор SQL-запросов предметной области (ПР7)
-- ============================================================

-- ============================================================
-- РАЗДЕЛ 1. Выборка списков объектов (SELECT, FROM, ORDER BY)
-- ============================================================

-- Запрос 1: Получение полного перечня оборудования с сортировкой по названию
SELECT
    id,
    name,
    category,
    model,
    serial_number,
    location,
    status
FROM equipment
ORDER BY name ASC;

-- Запрос 2: Получение списка всех сотрудников с сортировкой по отделу и ФИО
SELECT
    id,
    name,
    department,
    email
FROM employees
ORDER BY department ASC, name ASC;


-- ============================================================
-- РАЗДЕЛ 2. Фильтрация данных (WHERE, операторы сравнения и логики)
-- ============================================================

-- Запрос 3: Выборка оборудования, находящегося в состоянии эксплуатации
SELECT
    id,
    name,
    category,
    location,
    status
FROM equipment
WHERE status = 'в эксплуатации'
ORDER BY name;

-- Запрос 4: Выборка всех активных (незавершенных) операций
SELECT
    id,
    equipment_id,
    employee_id,
    operation_type,
    date,
    note
FROM operations
WHERE is_completed = 0
ORDER BY date DESC;

-- Запрос 5: Поиск операций типа «выдача», проведенных с сентября 2026 года
SELECT
    id,
    equipment_id,
    employee_id,
    operation_type,
    date
FROM operations
WHERE operation_type = 'выдача'
  AND date >= '2026-09-01'
ORDER BY date DESC;


-- ============================================================
-- РАЗДЕЛ 3. Соединение связанных таблиц (JOIN, LEFT JOIN, подзапросы)
-- ============================================================

-- Запрос 6: Полный журнал операций со сведениями об оборудовании и ответственном сотруднике
SELECT
    o.id AS operation_id,
    o.date AS operation_date,
    o.operation_type,
    o.note,
    o.is_completed,
    e.id AS equipment_id,
    e.name AS equipment_name,
    e.serial_number,
    e.category,
    emp.id AS employee_id,
    emp.name AS employee_name,
    emp.department AS employee_department
FROM operations o
JOIN equipment e ON o.equipment_id = e.id
LEFT JOIN employees emp ON o.employee_id = emp.id
ORDER BY o.date DESC;

-- Запрос 7: Поиск доступного оборудования (не находящегося в процессе активного ремонта)
SELECT
    e.id,
    e.name,
    e.category,
    e.model,
    e.location,
    e.status
FROM equipment e
WHERE e.id NOT IN (
    SELECT o.equipment_id
    FROM operations o
    WHERE o.operation_type = 'ремонт'
      AND o.is_completed = 0
)
ORDER BY e.name;


-- ============================================================
-- РАЗДЕЛ 4. Агрегирующие функции (COUNT, вычисление итоговых метрик)
-- ============================================================

-- Запрос 8: Подсчет общего количества единиц оборудования и техники в эксплуатации
SELECT
    COUNT(*) AS total_equipment,
    COUNT(CASE WHEN status = 'в эксплуатации' THEN 1 END) AS in_use_count,
    COUNT(CASE WHEN status = 'неисправно' THEN 1 END) AS broken_count
FROM equipment;

-- Запрос 9: Подсчет количества активных операций в журнале
SELECT
    COUNT(*) AS active_operations_count
FROM operations
WHERE is_completed = 0;


-- ============================================================
-- РАЗДЕЛ 5. Группировка и фильтрация групп (GROUP BY, HAVING)
-- ============================================================

-- Запрос 10: Распределение количества оборудования по категориям
SELECT
    category,
    COUNT(*) AS equipment_count
FROM equipment
GROUP BY category
ORDER BY equipment_count DESC, category ASC;

-- Запрос 11: Количество операций по каждой единице оборудования (включая единицы без операций)
SELECT
    e.id AS equipment_id,
    e.name AS equipment_name,
    e.category,
    COUNT(o.id) AS operations_count
FROM equipment e
LEFT JOIN operations o ON e.id = o.equipment_id
GROUP BY e.id, e.name, e.category
ORDER BY operations_count DESC, e.name ASC;

-- Запрос 12: Сотрудники, ответственные за более чем одну операцию (фильтрация групп HAVING)
SELECT
    emp.id AS employee_id,
    emp.name AS employee_name,
    emp.department,
    COUNT(o.id) AS operations_count
FROM employees emp
JOIN operations o ON emp.id = o.employee_id
GROUP BY emp.id, emp.name, emp.department
HAVING COUNT(o.id) > 1
ORDER BY operations_count DESC;
