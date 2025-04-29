import random

class Card:
    def __init__(self, value, suit):
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

    def more(self, other_card):
        index_value_card1 = Deck.values.index(self.value)
        index_value_card2 = Deck.values.index(other_card.value)
        if index_value_card1 > index_value_card2:
            return True
        elif index_value_card1 < index_value_card2:
            return False
        else: # Значения карт равны
            index_suit_card1 = Deck.suits.index(self.suit)
            index_suit_card2 = Deck.suits.index(other_card.suit)
            return  index_suit_card1 > index_suit_card2

    def less(self, other_card):
        return not self.more(other_card)


class Deck:
    values = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
    suits = ("Clubs", "Spades", "Diamonds", "Hearts")
    def __init__(self):
        self.cards = []
        for suit in Deck.suits:
            for value in Deck.values:
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
# card1 = Card("10", "Diamonds")
# card2 = Card("10", "Spades")

# Тестируем методы .less() и .more()
if card1.more(card2):
    print(f"{card1.to_str()} больше {card2.to_str()}")
if card1.less(card2):
    print(f"{card1.to_str()} меньше {card2.to_str()}")
