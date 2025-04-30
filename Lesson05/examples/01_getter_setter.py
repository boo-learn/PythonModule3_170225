class Circle:
    """
    Класс, представляющий окружность с возможностью управления радиусом
    через геттер (@property) и сеттер.
    """
    def __init__(self, radius):
        """
        Инициализирует объект окружности с заданным радиусом.
        """
        self._radius = radius  # Используем одинарное подчеркивание для обозначения "защищенного" атрибута

    @property
    def radius(self):
        """
        Геттер для получения значения радиуса окружности.

        Этот метод вызывается, когда вы пытаетесь получить доступ к атрибуту 'radius'
        объекта Circle (например, circle.radius).
        """
        return self._radius

    @radius.setter
    def radius(self, new_radius):
        """
        Сеттер для установки нового значения радиуса окружности.

        Этот метод вызывается, когда вы пытаетесь присвоить значение атрибуту 'radius'
        объекта Circle (например, circle.radius = 10).

        Здесь мы можем добавить логику проверки значения перед его установкой.
        """
        if not isinstance(new_radius, (int, float)):
            raise TypeError("Радиус должен быть числом")
        if new_radius <= 0:
            raise ValueError("Радиус должен быть положительным числом")
        self._radius = new_radius

    def area(self):
        """
        Вычисляет площадь окружности.
        """
        return 3.14159 * (self._radius ** 2)

# Пример использования класса Circle
if __name__ == "__main__":
    circle = Circle(5)

    # Получение радиуса с помощью геттера
    print(f"Начальный радиус: {circle.radius}")

    # Вычисление площади
    print(f"Площадь: {circle.area()}")

    # Изменение радиуса с помощью сеттера
    circle.radius = 10
    print(f"Новый радиус: {circle.radius}")
    print(f"Новая площадь: {circle.area()}")

    # Попытка установить некорректный радиус
    try:
        circle.radius = "abc"
    except TypeError as e:
        print(f"Ошибка: {e}")

    try:
        circle.radius = -2
    except ValueError as e:
        print(f"Ошибка: {e}")