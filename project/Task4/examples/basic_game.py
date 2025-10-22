from project.Task4 import (
    Player,
    BlackjackGame,
    ConservativeStrategy,
    AggressiveStrategy,
    BasicStrategy,
)


def main():
    """Run a basic Blackjack game."""
    print("=" * 70)
    print("BLACKJACK GAME - Basic Example")
    print("=" * 70)
    print()

    players = [
        Player("Conservative Bot", ConservativeStrategy()),
        Player("Aggressive Bot", AggressiveStrategy()),
        Player("Basic Strategy Bot", BasicStrategy()),
    ]

    game = BlackjackGame(players, max_rounds=5, num_decks=2)

    print("Starting a 5-round game with 3 bots using different strategies:\n")
    print("1. Conservative Bot - Stands on 12 or higher")
    print("2. Aggressive Bot - Hits until 17 or higher")
    print("3. Basic Strategy Bot - Uses optimal mathematical strategy")
    print()

    game.play_game(verbose=True)


if __name__ == "__main__":
    main()
