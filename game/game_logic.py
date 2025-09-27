import random
from .utils import rotate_list


def draw_card_from_player(receiver, giver):
    if not giver.hand:
        raise ValueError(f"player {giver} has no cards in hand")
    print(f"{receiver.name} is drawing from {giver.name}")
    if receiver.is_human:
        # Show the human player's hand
        print("\n🫴 Your hand:")
        for idx, card in enumerate(receiver.hand, start=1):
            print(f"{idx}. {card}")

        print(f"\n{giver.name} has {len(giver.hand)} cards.")
        print(f"{receiver.name}, pick a number between 1 and {len(giver.hand)} to draw a card.")
        while True:
            try:
                choice = int(input("Pick a card position: ")) - 1
            except ValueError:
                print("Please enter a valid number.")
            else:
                if not 0 <= choice < len(giver.hand):
                    print("Invalid number. Try again.")
                else:
                    break
    else:
        choice = random.randint(0, len(giver.hand) - 1)

    print(f"card in position {choice} has been chosen")
    drawn_card = giver.get_card_from_hand(choice)

    if drawn_card is None:
        raise ValueError(f"{receiver.name} drew an empty card")
    if not boomerang_check(receiver, giver, drawn_card):
        print(f"{receiver.name} drew the card {drawn_card.name} from {giver.name}.")


def give_card_to_player(receiver, giver):
    if not giver.hand:
        raise ValueError(f"player {giver} has no cards in hand")
    print(f"{giver.name} is giving a card to {receiver.name}")
    if giver.is_human:
        # Show the human player's hand
        print("\n🫴 Your hand:")
        for idx, card in enumerate(giver.hand, start=1):
            print(f"{idx}. {card}")

        print(f"{giver.name}, pick a number between 1 and {len(giver.hand)} to pick a card.")
        while True:
            try:
                choice = int(input("Pick a card position in your hand: ")) - 1
            except ValueError:
                print("Please enter a valid number.")
            else:
                if not 0 <= choice < len(giver.hand):
                    print("Invalid number. Try again.")
                else:
                    break
    elif giver.is_stinky_in_hand():
        choice = giver.get_position_of_card_in_hand_by_type("stinky")
    else:
        choice = random.randint(0, len(giver.hand)-1)

    print(f"card in position {choice + 1} has been chosen")
    picked_card = giver.get_card_from_hand(choice)

    if picked_card is None:
        raise ValueError(f"{giver.name} picked an empty card")
    if not boomerang_check(receiver, giver, picked_card):
        print(f"{giver.name} gave the card {picked_card.name} to {receiver.name}.")


def boomerang_check(receiver, giver, card):
    check = use_boomerang(receiver, card)
    if check:
        receiver.remove_card(receiver.get_card_of_type_from_hand("boomerang"))
        print(f"{receiver.name} used the boomerang and returned the sock back to {giver.name}")
    else:
        giver.remove_card(card)
        receiver.add_card(card)
    return check


def use_boomerang(player, drawn_card):
    choice = False
    if "boomerang" in list(card.type for card in player.hand):
        if player.is_human:
            # Show the human player's hand
            print("\n🫴 Your hand:")
            for idx, card in enumerate(player.hand, start=1):
                print(f"{idx}. {card}")
            print(f"{player.name},The card you received is {drawn_card}. Do you want to use the boomerang sock?")
            try:
                choice = bool(int(input("Write 0 or 1: ")))
                if not 0 <= choice <= 1:
                    print("Invalid answer. Try again.")
            except ValueError:
                print("Please enter a valid number.")
        else:
            choice = drawn_card.type == "stinky"
    return choice


def play_game(game):
    num_players = len(game.players)
    cards_per_player = 6 if num_players < 6 else 5
    main_deck = game.main_deck
    special_deck = game.special_deck
    '''is_player_active = dict()
    for player in game.players:
        is_player_active[player] = True 
    players = [player for player in is_player_active.keys() if is_player_active[player]]'''
    players = game.active_players
    
    # Initial deal
    refill_hands_repeat(game, players, cards_per_player)

    print("\n🧦 Game Start! 🧦")
    game.print_game_state()

    while game.active:
        current = players[game.current_player_index]
        next_player_index = (game.current_player_index + 1) % len(players)
        target = players[next_player_index]

        # Current player draws from its neighbor
        print(f"\n{current.name}'s turn. Drawing from {target.name}...")
        draw_card_from_player(current, target)
        game.print_game_state()

        # Check for pairs for current player
        if check_for_pairs([current]):
            '''pairs = current.find_pairs_in_hand()
            affected_players = []
            if pairs:
            print(f"{current.name} found and discarded pair(s): {', '.join(pairs)}")
            print_game_state(game)'''
            affected_players = [current, target]
        else:
            if len(game.active_players) > 2:
                special_card = special_deck.draw()
                print(f"{current.name} has no pairs.\nThe card {special_card.name} has been drawn from the special deck")
                activate_special_card(game, current, special_card.name)
                affected_players = rotate_list(players, game.current_player_index)
            else:
                affected_players = [target]

        # Refill hands to relevant players to maintain card count and check for pairs again
        if not main_deck.is_empty():
            refill_hands_repeat(game, affected_players, cards_per_player)

        # Check for players with only boomerang in hand
        for player in players:
            if player.has_only_boomerang_in_hand() and not player.is_hand_empty():
                print(f"player {player.name} has only boomerang card in hand and discarded his hand.")
                player.discard_hand()

        # End turn checks
        for player in rotate_list(players, game.current_player_index):
            if player.is_hand_empty():
                players.remove(player)
                print(f"{player.name} has won")

        # Check for endgame
        # players = [player for player in is_player_active.keys() if is_player_active[player]]
        if len(players) == 1:
            last = players[0]
            print(f"\n💩 {last.name} is left with the Stinky Sock! He loses.")
            game.active = False
            break

        # Advance turn
        game.next_player()
        print(f"---------- NEXT ROUND ----------")


def check_for_pairs(players):
    found = False
    for player in players:
        pairs = player.find_pairs_in_hand()
        if pairs:
            found = True
            print(f"{player.name} found and discarded pair(s): {', '.join(pairs)}")
    return found


def refill_hands(players, cards_per_player, deck):
    empty_main_deck = False
    for player in players:
        while len(player.hand) < cards_per_player and not empty_main_deck:
            drawn_card = deck.draw()
            print(f"{player.name} has {len(player.hand)} cards in hand")
            if drawn_card:
                player.add_card(drawn_card)
                print(f"{player.name} drew the card {drawn_card.name}")
            else:
                empty_main_deck = True
                print(f"The main deck is now empty")


def refill_hands_repeat(game, players, cards_per_player):
    game.print_game_state()
    while not game.main_deck.is_empty() and players:
        print(f"Refilling the hand of {[player.name for player in players]}")
        refill_hands(players, cards_per_player, game.main_deck)
        another_round = []
        for player in players:
            pairs = player.find_pairs_in_hand()
            if pairs:
                print(f"{player.name} found and discarded pair(s): {', '.join(pairs)}")
                another_round.append(player)
        players = another_round


#########################################
###########   Special cards   ###########
#########################################


def activate_special_card(game, current_player, name):
    match name:
        case "Birthday":
            activate_birthday(game, current_player)
        case _:
            raise ValueError(f"The special card {name} doesn't exist")


def activate_birthday(game, current_player):
    other_players = game.active_players.copy()
    other_players.remove(current_player)
    for player in other_players:
        give_card_to_player(current_player, player)
    check_for_pairs([current_player])


def activate_bruise(game, current_player):
    pass

