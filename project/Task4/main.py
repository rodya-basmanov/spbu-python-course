from project.Task4.game import BlackjackGame
from project.Task4.player import Player
from project.Task4.strategy import (
    ConservativeStrategy,
    AggressiveStrategy,
    DealerStrategy,
)


def main():
    print("BLACKJACK GAME")
    print()

    players = [
        Player("Bot 1", ConservativeStrategy()),
        Player("Bot 2", AggressiveStrategy()),
        Player("Bot 3", DealerStrategy()),
    ]

    print("Players:")
    for p in players:
        print(f"  - {p.name} ({p.strategy.get_name()} strategy)")
    print()

    game = BlackjackGame(players, rounds=5)
    game.play()

    print()
    print("GAME FINISHED")


if __name__ == "__main__":
    main()
