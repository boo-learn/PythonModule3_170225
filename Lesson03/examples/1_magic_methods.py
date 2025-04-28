# Магические методы - это специальные методы, имена которых начинаются и заканчиваются двумя подчеркиваниями (__).
# Они вызываются не напрямую, а интерпретатором Python в определенных ситуациях.
# Они позволяют определить, как объекты вашего класса взаимодействуют со встроенными операторами и функциями Python.

class MyNumber:
    def __init__(self, value):
        """
        Конструктор класса. Вызывается при создании нового объекта.
        Здесь мы инициализируем атрибут 'value'.
        """
        self.value = value

    def __str__(self):
        """
        Вызывается функцией str() для создания "неформального" строкового представления объекта.
        Полезно для вывода объекта на экран.
        """
        return f"Мое число: {self.value}"

    def __repr__(self):
        """
        Вызывается функцией repr() для создания "официального" строкового представления объекта.
        В идеале, это должна быть строка, из которой можно восстановить объект.
        Часто, если __str__ не определен, используется __repr__.
        """
        return f"MyNumber({self.value})"

    def __add__(self, other):
        """
        Вызывается при использовании оператора сложения (+).
        Определяет, что произойдет, когда два объекта MyNumber будут сложены.
        """
        if isinstance(other, MyNumber):
            return MyNumber(self.value + other.value)
        elif isinstance(other, (int, float)):
            return MyNumber(self.value + other)
        else:
            return NotImplemented  # Возвращаем NotImplemented, если операция не поддерживается с данным типом

    def __sub__(self, other):
        """
        Вызывается при использовании оператора вычитания (-).
        Определяет, что произойдет, когда один объект MyNumber вычитается из другого.
        """
        if isinstance(other, MyNumber):
            return MyNumber(self.value - other.value)
        elif isinstance(other, (int, float)):
            return MyNumber(self.value - other)
        else:
            return NotImplemented

    def __mul__(self, other):
        """
        Вызывается при использовании оператора умножения (*).
        Определяет, что произойдет, когда объект MyNumber умножается на что-то.
        """
        if isinstance(other, MyNumber):
            return MyNumber(self.value * other.value)
        elif isinstance(other, (int, float)):
            return MyNumber(self.value * other)
        else:
            return NotImplemented

    def __eq__(self, other):
        """
        Вызывается при использовании оператора равенства (==).
        Определяет, равны ли два объекта MyNumber.
        """
        if isinstance(other, MyNumber):
            return self.value == other.value
        elif isinstance(other, (int, float)):
            return self.value == other
        else:
            return NotImplemented

    def __lt__(self, other):
        """
        Вызывается при использовании оператора "меньше чем" (<).
        Определяет, является ли один объект MyNumber меньше другого.
        """
        if isinstance(other, MyNumber):
            return self.value < other.value
        elif isinstance(other, (int, float)):
            return self.value < other
        else:
            return NotImplemented

    def __len__(self):
        """
        Вызывается функцией len().
        Этот метод обычно используется для контейнеров (списков, строк и т.д.),
        но мы можем определить его и для других классов, если это имеет смысл.
        В данном случае, мы можем вернуть 1, считая, что объект "содержит" одно значение.
        """
        return 1

    def __getitem__(self, key):
        """
        Вызывается при попытке доступа к элементу объекта по индексу или ключу (например, obj[key]).
        Этот метод делает объект "похожим" на последовательность или словарь.
        В нашем случае, мы можем вернуть значение, если ключ равен 0.
        """
        if key == 0:
            return self.value
        else:
            raise IndexError("Индекс за пределами допустимого диапазона")

    def __setitem__(self, key, new_value):
        """
        Вызывается при попытке присвоить значение элементу объекта по индексу или ключу (например, obj[key] = value).
        Этот метод позволяет изменять "элементы" объекта.
        В нашем случае, мы можем изменить значение, если ключ равен 0.
        """
        if key == 0:
            self.value = new_value
        else:
            raise IndexError("Индекс за пределами допустимого диапазона")

    def __delitem__(self, key):
        """
        Вызывается при попытке удалить элемент объекта по индексу или ключу (например, del obj[key]).
        В нашем простом примере с одним значением удаление не имеет особого смысла,
        но мы можем выбросить исключение.
        """
        raise TypeError("Удаление элемента не поддерживается для MyNumber")

    def __iter__(self):
        """
        Вызывается при использовании функции iter() для создания итератора для объекта.
        Этот метод делает объект итерируемым (можно использовать в цикле for).
        Мы можем сделать так, чтобы объект выдавал свое значение один раз.
        """
        yield self.value

    def __contains__(self, item):
        """
        Вызывается при использовании оператора in для проверки, содержится ли элемент в объекте.
        """
        return item == self.value

    # Другие полезные магические методы:
    # __new__(cls, *args, **kwargs) - вызывается перед __init__, отвечает за создание экземпляра класса.
    # __del__(self) - вызывается при удалении объекта сборщиком мусора (не рекомендуется часто использовать).
    # __getattr__(self, name) - вызывается при попытке доступа к несуществующему атрибуту.
    # __setattr__(self, name, value) - вызывается при присваивании значения атрибуту.
    # __delattr__(self, name) - вызывается при удалении атрибута.
    # __call__(self, *args, **kwargs) - позволяет вызывать объект как функцию.
    # __enter__(self) и __exit__(self, exc_type, exc_val, exc_tb) - используются для управления контекстными менеджерами (with statement).
    # __hash__(self) - вызывается встроенной функцией hash() и используется в структурах данных на основе хеш-таблиц (например, словари, множества).
    # __bool__(self) - вызывается при проверке истинности объекта (например, в операторах if).


# Пример использования
num1 = MyNumber(10)
num2 = MyNumber(5)

print(num1)  # Вызывает __str__
print(repr(num1))  # Вызывает __repr__

sum_num = num1 + num2  # Вызывает __add__
print(f"Сумма: {sum_num}")

diff_num = num1 - num2  # Вызывает __sub__
print(f"Разность: {diff_num}")

prod_num = num1 * 2  # Вызывает __mul__
print(f"Произведение: {prod_num}")

print(num1 == MyNumber(10))  # Вызывает __eq__
print(num1 < num2)  # Вызывает __lt__

print(len(num1))  # Вызывает __len__

print(num1[0])  # Вызывает __getitem__
num1[0] = 20  # Вызывает __setitem__
print(num1)
# del num1[0]         # Вызывает __delitem__ (вызовет ошибку)

for value in num1:  # Вызывает __iter__
    print(f"Итерация: {value}")

print(10 in num1)  # Вызывает __contains__
print(5 in num1)  # Вызывает __contains__
