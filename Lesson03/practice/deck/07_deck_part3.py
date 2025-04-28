import random

class Card:
    def __init__(self, value, suit):
        '2' '3' '4'
        self.value = value  # Значение карты(2, 3... 10, J, Q, K, A)
        self.suit = suit  # Масть карты

    def to_str(self):
        icons = {
            "Diamonds": '\u2666',
            "Hearts": "\u2665",
            "Spades": '\u2660',
            "Clubs": '\u2663'
        }
        return f"{self.value}{icons[self.suit]}"

    def equal_suit(self, other_card):
        return self.suit == other_card.suit

    # TODO-1: реализуем новые методы
    def more(self, other_card):
        ...

    def less(self, other_card):
        ...


class Deck:
    def __init__(self):
        #          0    1    2 ....
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        #          0          1         2         3
        suits = ["Clubs", "Spades","Diamonds","Hearts"]
        self.cards = []
        for suit in suits:
            for value in values:
                card = Card(value, suit)
                self.cards.append(card)

    def show(self):
        cards_str = []
        for card in self.cards:
            cards_str.append(card.to_str())
        return f"deck[{len(self.cards)}]:" + ", ".join(cards_str)

    def draw(self, x) -> list:
        hand = self.cards[:x]
        self.cards = self.cards[x:]
        return hand

    def shuffle(self) -> None:
        random.shuffle(self.cards)


# Создаем колоду
deck = Deck()
# Тусуем колоду
deck.shuffle()
print(deck.show())
# Берем две карты из колоды
card1, card2 = deck.draw(2)

# Тестируем методы .less() и .more()
if card1.more(card2):
    print(f"{card1.to_str()} больше {card2.to_str()}")
if card1.less(card2):
    print(f"{card1.to_str()} меньше {card2.to_str()}")
