class GameState:
    def __init__(self, players, main_deck, special_deck):
        self.players = players.copy()
        self.active_players = players.copy()
        self.main_deck = main_deck
        self.special_deck = special_deck
        self.current_player_index = 0
        self.active = True

    def next_player(self):
        for i in range(len(self.active_players)):
            self.current_player_index = (self.current_player_index + 1) % len(self.active_players)
            player = self.players[self.current_player_index]
            return player
        raise ValueError(f"There is no next player")

    def print_game_state(self):
        print(f'Main deck: {self.main_deck.count()}')
        print(f'Active players: {[player.name for player in self.active_players]}')
        for player in self.active_players:
            print(f'{player.name} has {len(player.hand)} cards.')
            print(f'{player.name} hand: {player.hand}')
