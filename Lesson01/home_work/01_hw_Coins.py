# # Задание:
# 1. Создайте список из n-монеток, n - вводится с клавиатуры
# 2. Подбросьте(flip) все монетки. У каждой монетки в списке вызовите метод .flip()
# 3. Выведите соотношение выпавших орлов и решек в процентах
#
# Пояснение: когда вы создаете монетку, то она находится в неопределенном состоянии self.side = None, т.е.
# она находится у вас в руке и не выпала ни орлом ни решкой. \
# Монетка "определеяется" со стороной(орел/решка), только после того, как вы ее подбрасываете(вызываете метод flip())


import random


class Coin:
    def __init__(self):
        self.side = None

    def flip(self) -> None:
        """
        Подбрасывание монетки. # heads-орел/tails-решка
        """
        self.side = random.choice(["heads", "tails"])


n = int(input("Количество монеток : "))
coins = [Coin() for i in range(n)]

# coins = []
# for i in range(n):
#     coin = Coin()
#     coins.append(coin)

for coin in coins:
    coin.flip()

heads = 0
tails = 0
for coin in coins:
    if coin.side == "heads":
        heads += 1
    else:
        tails += 1

heads_percent = heads / (heads + tails) * 100
tails_percent = tails / (heads + tails) * 100

print(f" % heads: {heads_percent} | % tails {tails_percent}")



