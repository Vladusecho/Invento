"""Вспомогательные функции ввода."""


def input_int(prompt: str) -> int:
    """Безопасный ввод целого числа."""
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("❌ Введите целое число.")


def input_str(prompt: str) -> str:
    """Безопасный ввод непустой строки."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("❌ Поле не может быть пустым.")