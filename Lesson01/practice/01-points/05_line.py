from __future__ import annotations


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def dist_to(self, other_point: Point) -> float:
        return ((self.x - other_point.x) ** 2 + (self.y - other_point.y) ** 2) ** 0.5


# Ломаная линия задана произвольным количеством последовательных точек
points = [Point(2, 4), Point(7, 5), Point(5, -2), Point(0, 6), Point(-12, 0)]

total_distance = 0
num_points = len(points)
for i in range(num_points - 1):
    # print(i, ":", i + 1)
    point1 = points[i]
    point2 = points[i + 1]
    total_distance += point1.dist_to(point2)

print("Длина ломаной линии = ", total_distance)
