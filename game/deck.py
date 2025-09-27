import random
from .card import Card, PairedSockCard
from .utils import rotate_list


CARDS_COLORS = ['blue', 'green', 'orange', 'black', 'pink', 'yellow', 'purple', 'red', 'white']
NUMBER_OF_SOCKS = 15


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
        cards_colors = random_sock_colors()
        if self.name == "main":
            # 20 pairs of socks
            # deck = [Card(f"Sock-{i}") for i in range(1, 21) for _ in range(2)]
            deck = []
            for j in range(NUMBER_OF_SOCKS):
                deck += [PairedSockCard(f"Sock-{j+1}", cards_colors[2*j], cards_colors[2*j+1])]
                deck += [PairedSockCard(f"Sock-{j+1}", cards_colors[2 * j], cards_colors[2*j+1])]
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


def random_sock_colors():
    indices = [random.randint(0, len(CARDS_COLORS)-1) for _ in (range(NUMBER_OF_SOCKS*2))]
    return [CARDS_COLORS[indices[i]] for i in (range(NUMBER_OF_SOCKS*2))]
