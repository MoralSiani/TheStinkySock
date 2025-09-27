class Card:
    def __init__(self, name, card_type):
        self.name = name
        self.type = card_type

    def __repr__(self):
        return f"{self.name}"


class PairedSockCard(Card):
    def __init__(self, name, color1, color2, card_type="sock"):
        super().__init__(name, card_type)
        self.color1 = color1
        self.color2 = color2

    def __repr__(self):
        return f"{self.name} - {self.color1}/{self.color2}"
