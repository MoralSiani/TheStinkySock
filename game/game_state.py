class GameState:
    def __init__(self, players, main_deck, special_deck):
        self.players = players
        self.main_deck = main_deck
        self.special_deck = special_deck
        self.current_player_index = 0
        self.active = True

    def next_player(self, is_player_active):
        for i in range(len(self.players)):
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            player = self.players[self.current_player_index]
            if is_player_active[player]:
                return player
        raise ValueError(f"There is no next player")
