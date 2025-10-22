from project.Task4 import (
    Player,
    BlackjackGame,
    ConservativeStrategy,
    AggressiveStrategy,
    DealerStrategy,
)


def main():
    """Run a detailed single-round game."""
    print("=" * 70)
    print("BLACKJACK GAME - Single Round Detailed Example")
    print("=" * 70)
    print()

    players = [
        Player("Conservative Bot", ConservativeStrategy()),
        Player("Aggressive Bot", AggressiveStrategy()),
        Player("Dealer-like Bot", DealerStrategy()),
    ]

    game = BlackjackGame(players, max_rounds=1, num_decks=1)

    print("Players in the game:")
    for player in players:
        print(f"  - {player.name} (Strategy: {player.strategy.get_name()})")
    print()

    print("Starting the round...\n")
    game.current_round = 1

    print("=" * 70)
    print("STEP 1: Dealing Initial Cards")
    print("=" * 70)
    game.deal_initial_cards()
    print(game.show_game_state())
    print()

    print("=" * 70)
    print("STEP 2: Players' Turn")
    print("=" * 70)
    print()

    dealer_upcard = game.dealer.get_upcard()
    print(f"Dealer's upcard: {dealer_upcard}\n")

    for player in players:
        print(f"\n{player.name}'s turn:")
        print(f"  Initial hand: {player.hand}")

        while player.should_hit(dealer_upcard):
            card = game.deck.draw_card()
            player.receive_card(card)
            print(f"  Hit: received {card}")
            print(f"  Current hand: {player.hand}")

            if player.is_busted():
                print(f"  BUSTED! (value: {player.get_hand_value()})")
                break

        if not player.is_busted() and player.is_active:
            player.stand()
            print(f"  STAND (value: {player.get_hand_value()})")

    print(f"\n{'-' * 70}\n")

    print("=" * 70)
    print("STEP 3: Dealer's Turn")
    print("=" * 70)
    print()
    print(f"Dealer's hand: {game.dealer.hand}")

    any_player_active = any(not player.is_busted() for player in players)

    if any_player_active:
        while game.dealer.should_hit():
            card = game.deck.draw_card()
            game.dealer.receive_card(card)
            print(f"Dealer hits: received {card}")
            print(f"Dealer's hand: {game.dealer.hand}")

            if game.dealer.is_busted():
                print(f"Dealer BUSTED! (value: {game.dealer.get_hand_value()})")
                break

        if not game.dealer.is_busted():
            print(f"Dealer stands (value: {game.dealer.get_hand_value()})")
    else:
        print("All players busted - dealer doesn't play")

    print(f"\n{'-' * 70}\n")

    print("=" * 70)
    print("STEP 4: Determining Winners")
    print("=" * 70)
    print()

    game.state = game.get_state()
    winners = game.determine_winners()

    print(game.show_game_state())
    print()

    if winners:
        print(f"🏆 Winners: {', '.join(winners)}")
    else:
        print("🤝 No winners this round (all players busted or tied)")

    print()
    print("=" * 70)
    print("Game Complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
