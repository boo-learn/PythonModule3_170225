class People:
    def __init__(self, name: str, surname: str, age: int):
        self.name = name
        self.surname = surname
        self.age = age

    def full_name(self) -> str:
        return f"{self.surname} {self.name}"



# Создадим двух человек:
people1 = People("Иван", "Уткин", 27)
people2 = People("Алексей", "Перов", 35)

# Выведем данные о человеке, используя метод full_name:

...
