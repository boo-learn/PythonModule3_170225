class Item:
    def __init__(self, name: str, weight: float, cost: int):
        self.name = name  # Название предмета
        self.weight = weight  # Вес предмета, в килограммах
        self.cost = cost  # Цена предмета, пусть будет, в рублях

    def show(self) -> str:
        """
        Возвращает строковое представление объекта Item
        """
        return f"{self.name} вес:{self.weight} цена:{self.cost}"


# TODO-1: Дополните конструктор класса Item
item1 = Item("Гиря", 25, 500)
item2 = Item("Арбуз", 4, 300)
item3 = Item("Ноутбук", 2.5, 22500)
item4 = Item("Кот", 0.5, 250)

# TODO-3: сделайте функцию show_item(), методом show() класса Item
print(item1.show())
print(item2.show())
print(item3.show())
print(item4.show())

# Помещаем все объекты item в список:
items = [item1, item2, item3, item4]
# TODO-4:  Выведите элементы в виде нумерованного списка, при выводе используйте метод .show()
for i, item in enumerate(items, 1):
    print(i, item.show())
