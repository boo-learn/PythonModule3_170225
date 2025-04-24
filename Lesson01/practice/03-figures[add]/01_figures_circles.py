import math


class Circle:
    def __init__(self, center_coords, radius):
        self.center = center_coords
        self.radius = radius

    def length(self):
        """
        :return: длину окружности
        """
        return 2 * math.pi * self.radius

    def area(self):
        """
        :return: площадь окружности
        """
        return math.pi * self.radius ** 2

    def move_to(self):
        ...


# Окружности заданы координатами центров и радиусами
circle1 = Circle((6, -8), 5)
circle2 = Circle((2, 4), 4)

circle1.area()

print(f"Длина окружности радиусом {...} = {...}")
print(f"Длина окружности радиусом {...} = {...}")

print(f"Площадь окружности радиусом {...} = {...}")
print(f"Площадь окружности радиусом {...} = {...}")
