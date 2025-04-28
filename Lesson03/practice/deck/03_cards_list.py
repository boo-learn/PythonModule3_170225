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



values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
hearts_cards = []
for value in values:
    card = Card(value, "Hearts")
    hearts_cards.append(card)

diamonds_cards = []
for value in values:
    card = Card(value, "Diamonds")
    diamonds_cards.append(card)

hearts_string = ""
for card in hearts_cards:
    hearts_string += card.to_str() + ", "

print(hearts_string)

#
# cards = [
#     Card("2", "Hearts"),
#     Card("3", "Hearts"),
#     Card("4", "Hearts"),
#     ...]