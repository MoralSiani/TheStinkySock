from game.deck import Deck, SpecialDeck
from game.player import Player
from game.game_state import GameState
from game.game_logic import play_game


def main():
    player_names = ["You", "AlinaBot", "GilaiBot", "TegalBot"]
    players = [Player("You", is_human=True)] + [Player(name) for name in player_names[1:]]

    main_deck = Deck()
    special_deck = SpecialDeck()
    game = GameState(players, main_deck, special_deck)
    play_game(game)


if __name__ == "__main__":
    main()
