class Money:
    def __init__(self, rub, kop):
        self.kop = rub * 100 + kop

    def __add__(self, other):
        new_money_sum = Money(0, self.kop + other.kop)
        return new_money_sum

    def __sub__(self, other):
        new_money_sum = Money(0, self.kop - other.kop)
        return new_money_sum

    def __mul__(self, other):
        return Money(0, self.kop * other)

    def normalize(self):
        has_minus = False
        if self.kop < 0:
            self.kop *= -1
            has_minus = True
        if self.kop >= 100:
            rub = self.kop // 100
            kop = self.kop % 100
        else:
            rub = 0
            kop = self.kop
        if has_minus:
            return -rub, kop
        return rub, kop

    def __str__(self):
        rub, kop = self.normalize()
        return f"{rub}руб {kop}коп"


# Создаем две денежные суммы
money_sum1 = Money(20, 60)  # 2060
money_sum2 = Money(30, 40)  # 1090

money_sum3 = money_sum1 + money_sum2 # -> money_sum1.__add__(money_sum1)
money_sum4 = money_sum1 - money_sum2  # -> money_sum1.__sub__(money_sum1)

money_sum5 = money_sum1 * 5 # money_sum1.__mul__(5)

print(money_sum1)
print(money_sum2)
print(money_sum3)
print(money_sum4)
print(money_sum5)

# Складываем суммы
# money_result = money_sum1 + money_sum2
# print(money_result)  # 31руб 5коп
