import random
from .card import Card
from .utils import rotate_list


class Deck:
    def __init__(self, name="main"):
        self.name = name
        self.cards = self.create_deck()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        if self.is_empty():
            return None
        return self.cards.pop()

    def is_empty(self):
        return len(self.cards) == 0

    def count(self):
        return len(self.cards)

    def peek_top(self):
        if not self.is_empty():
            return self.cards[-1]
        return None

    def print_deck(self):
        print(f"\n📦 {self.name} deck ({len(self.cards)} cards):")
        for idx, card in enumerate(self.cards, 1):
            print(f"{idx}. {card}")

    def create_deck(self):
        if self.name == "main":
            # 20 pairs of socks
            # deck = [Card(f"Sock-{i}") for i in range(1, 21) for _ in range(2)]
            deck = [Card(f"Sock-{i}") for i in range(1, 15) for _ in range(2)]
            deck += [Card("Boomerang Sock", "boomerang") for _ in range(2)]
            deck += [Card("Stinky Sock", "stinky")]
            random.shuffle(deck)
        elif self.name == "special":
            names = [
                "Birthday", "Birthday", "Birthday"
            ]
            '''names = [
                "Washing", "Washing", "Grandma", "Dog", "Bare leg", "Bruise", "Spy",
                "Hole", "New Year", "February 23", "Birthday"
            ]'''
            deck = [Card(name, "special") for name in names]
            random.shuffle(deck)
        else:
            raise ValueError(f"deck type {self.name} is invalid")
        return deck


class SpecialDeck(Deck):
    def __init__(self, name="special"):
        super().__init__(name)

    def draw(self):
        if self.is_empty():
            return None
        else:
            card = self.cards[0]
            self.cards = rotate_list(self.cards, 1)
            return card
