from project.Task4 import (
    Player,
    BlackjackGame,
    ConservativeStrategy,
    AggressiveStrategy,
    DealerStrategy,
    BasicStrategy,
    CautiousAggressiveStrategy,
)


def print_header():
    print("\n" + "=" * 70)
    print("🎮 BLACKJACK GAME 🎮")
    print("=" * 70)


def choose_strategies():
    strategies = {
        "1": ("Conservative", ConservativeStrategy, "Stands on 12 or higher"),
        "2": ("Aggressive", AggressiveStrategy, "Hits until 17 or higher"),
        "3": ("Dealer-like", DealerStrategy, "Standard casino dealer rules"),
        "4": ("Basic", BasicStrategy, "Optimal mathematical strategy"),
        "5": (
            "Cautious-Aggressive",
            CautiousAggressiveStrategy,
            "Adapts to dealer's upcard",
        ),
    }

    print("\n📋 Available Bot Strategies:")
    print("-" * 70)
    for key, (name, _, description) in strategies.items():
        print(f"{key}. {name:20s} - {description}")
    print("-" * 70)

    return strategies


def get_number_input(prompt, min_val, max_val, default=None):
    while True:
        try:
            if default:
                user_input = input(f"{prompt} (default: {default}): ").strip()
                if not user_input:
                    return default
                value = int(user_input)
            else:
                value = int(input(f"{prompt}: ").strip())

            if min_val <= value <= max_val:
                return value
            else:
                print(f"❌ Please enter a number between {min_val} and {max_val}")
        except ValueError:
            print("❌ Please enter a valid number")


def main():
    print_header()

    print("\n🎯 Game Setup\n")

    num_rounds = get_number_input(
        "Enter number of rounds (1-100)", min_val=1, max_val=100, default=5
    )

    num_decks = get_number_input(
        "Enter number of decks (1-8)", min_val=1, max_val=8, default=2
    )

    strategies = choose_strategies()

    num_bots = get_number_input(
        "\nHow many bots do you want? (1-10)", min_val=1, max_val=10, default=3
    )

    print("\n🤖 Configure Your Bots\n")

    players = []
    for i in range(num_bots):
        print(f"\nBot #{i+1}:")

        bot_name = input(f"  Enter bot name (default: Bot {i+1}): ").strip()
        if not bot_name:
            bot_name = f"Bot {i+1}"

        print(f"\n  Choose strategy for '{bot_name}':")
        for key, (name, _, description) in strategies.items():
            print(f"    {key}. {name}")

        while True:
            strategy_choice = input(
                f"  Enter strategy number (1-5, default: 4): "
            ).strip()
            if not strategy_choice:
                strategy_choice = "4"

            if strategy_choice in strategies:
                strategy_name, strategy_class, _ = strategies[strategy_choice]
                players.append(Player(bot_name, strategy_class()))
                print(f"  ✅ {bot_name} created with {strategy_name} strategy")
                break
            else:
                print("  ❌ Invalid choice, please try again")

    print("\n" + "=" * 70)
    print("🎮 GAME SUMMARY")
    print("=" * 70)
    print(f"Rounds: {num_rounds}")
    print(f"Decks: {num_decks}")
    print(f"\nPlayers:")
    for player in players:
        print(f"  • {player.name} ({player.strategy.get_name()})")
    print("=" * 70)

    input("\nPress ENTER to start the game...")

    game = BlackjackGame(players, max_rounds=num_rounds, num_decks=num_decks)
    game.play_game(verbose=True)

    print("\n" + "=" * 70)
    print("🎉 GAME FINISHED! 🎉")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Game cancelled by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
