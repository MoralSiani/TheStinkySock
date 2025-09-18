class Player:
    def __init__(self, name, is_human=False):
        self.name = name
        self.hand = []
        self.is_human = is_human

    def add_card(self, card):
        self.hand.append(card)

    def is_hand_empty(self):
        return not self.hand

    def remove_card(self, card):
        self.hand.remove(card)

    def remove_card_instances(self, card_name):
        self.hand = [c for c in self.hand if c.name != card_name]

    def get_card_from_hand(self, position):
        try:
            return self.hand[position]
        except IndexError:
            raise ValueError(f"card in position {position} does not exist")

    def get_card_of_type_from_hand(self, card_type):
        card_types = list(card.type for card in self.hand)
        if card_type in card_types:
            idx = card_types.index(card_type)
            return self.hand[idx]
        else:
            raise ValueError(f"No {card_type} card in hand")

    def get_position_of_card_in_hand_by_type(self, card_type):
        '''
        :param card_type:
        :return: Position of the first appearance of card_type in hand, else raises error
        '''
        card_types = list(card.type for card in self.hand)
        if card_type in card_types:
            idx = card_types.index(card_type)
            return idx
        else:
            raise ValueError(f"No {card_type} card in hand")

    def get_type_of_card_in_hand_by_position(self, position):
        '''
            :param position:
            :return: The type of the card in hand in the wanted position
        '''
        return self.hand[position].name

    def is_stinky_in_hand(self):
        card_types = list(card.type for card in self.hand)
        return "stinky" in card_types

    def find_pairs_in_hand(self):
        counts = {}
        pairs = []
        for card in self.hand:
            if card.type == "sock":
                counts[card.name] = counts.get(card.name, 0) + 1
                if counts[card.name] == 2:
                    pairs.append(card.name)
        for name in pairs:
            self.remove_card_instances(name)
        return pairs

    def discard_hand(self):
        self.hand = []

    def has_only_boomerang_in_hand(self):
        return all(card.type == "boomerang" for card in self.hand)
