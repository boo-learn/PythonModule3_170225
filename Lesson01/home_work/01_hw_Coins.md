# Задание:
1. Создайте список из n-монеток, n - вводится с клавиатуры
2. Подбросьте(flip) все монетки. У каждой монетки в списке вызовите метод .flip()
3. Выведите соотношение выпавших орлов и решек в процентах

Пояснение: когда вы создаете монетку, то она находится в неопределенном состоянии self.side = None, т.е.
она находится у вас в руке и не выпала ни орлом ни решкой. \
Монетка "определеяется" со стороной(орел/решка), только после того, как вы ее подбрасываете(вызываете метод flip())

```python
import random


class Coin:
    def __init__(self):
        self.side = None

    def flip(self) -> None:
        self.side = random.choice(["heads", "tails"])
        # random: heads/tails


n = int(input("Количество монеток : "))
coins = []
for coin in range(n):
    coins.append(Coin())
    coins[coin].flip()

for coin in coins:
    heads_coin = sum(1 for coin in coins if coin.side == "heads")
    tails_coin = len(coins) - heads_coin

total = len(coins)
heads = heads_coin / total
tails = tails_coin / total
print("ОРЁЛ -----------------Решка")
print(f' {heads}, <<----->> {tails}"')
