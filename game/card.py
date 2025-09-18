class Card:
    def __init__(self, name, card_type="sock"):
        self.name = name
        self.type = card_type

    def __repr__(self):
        return f"{self.name}"
