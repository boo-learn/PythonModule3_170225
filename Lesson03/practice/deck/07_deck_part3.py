import random


class Card:
    def __init__(self, value, suit):
        self.value = value  # Значение карты(2, 3... 10, J, Q, K, A)
        self.suit = suit  # Масть карты

    def __str__(self):
        icons = {
            "Diamonds": '\u2666',
            "Hearts": "\u2665",
            "Spades": '\u2660',
            "Clubs": '\u2663'
        }
        return f"{self.value}{icons[self.suit]}"

    def equal_suit(self, other_card):
        return self.suit == other_card.suit

    def __gt__(self, other_card):
        index_value_card1 = Deck.values.index(self.value)
        index_value_card2 = Deck.values.index(other_card.value)
        if index_value_card1 > index_value_card2:
            return True
        elif index_value_card1 < index_value_card2:
            return False
        else:  # Значения карт равны
            index_suit_card1 = Deck.suits.index(self.suit)
            index_suit_card2 = Deck.suits.index(other_card.suit)
            return index_suit_card1 > index_suit_card2

    def __lt__(self, other_card):
        return not self.__gt__(other_card)


class Deck:
    values = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
    suits = ("Clubs", "Spades", "Diamonds", "Hearts")

    def __init__(self):  # magic-method
        self.cards = []
        self.last_index_card = 0
        for suit in Deck.suits:
            for value in Deck.values:
                card = Card(value, suit)
                self.cards.append(card)

    def __str__(self):
        cards_str = []
        for card in self.cards:
            cards_str.append(card.__str__())
        return f"deck[{len(self.cards)}]:" + ", ".join(cards_str)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            card = self.cards[self.last_index_card]
        except IndexError:
            raise StopIteration
        self.last_index_card += 1
        return card

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

print(deck)
card1 = Card("Q", "Clubs")
card2 = Card("J", "Diamonds")
#
if card1 > card2:
    print(f"{card1} больше {card2}")

for card in deck:
    print(card)


# iterator = iter(deck)  # -> deck.__iter__()
# print(next(iterator))  # -> iterator.__next__()
# print(next(iterator))  # -> iterator.__next__()
# print(next(iterator))  # -> iterator.__next__()
# print(next(iterator))  # -> iterator.__next__()
