from project.Task4 import (
    Player,
    BlackjackGame,
    ConservativeStrategy,
    AggressiveStrategy,
    BasicStrategy,
    DealerStrategy,
    CautiousAggressiveStrategy,
)


def main():
    """Compare different strategies over many rounds."""
    print("=" * 70)
    print("BLACKJACK GAME - Strategy Comparison")
    print("=" * 70)
    print()

    players = [
        Player("Conservative", ConservativeStrategy()),
        Player("Aggressive", AggressiveStrategy()),
        Player("Dealer-like", DealerStrategy()),
        Player("Basic", BasicStrategy()),
        Player("Cautious-Aggressive", CautiousAggressiveStrategy()),
    ]

    print("Comparing 5 different bot strategies over 100 rounds:\n")
    for player in players:
        print(f"  - {player.name:20s} ({player.strategy.get_name()})")
    print()

    game = BlackjackGame(players, max_rounds=100, num_decks=6)

    print("Playing 100 rounds... (output suppressed for brevity)")
    print()
    stats = game.play_game(verbose=False)

    print("=" * 70)
    print("FINAL RESULTS")
    print("=" * 70)
    print()
    results = []
    for player_name, player_stats in stats.items():
        total = player_stats["wins"] + player_stats["losses"] + player_stats["draws"]
        win_rate = (player_stats["wins"] / total * 100) if total > 0 else 0
        results.append(
            (
                player_name,
                player_stats["wins"],
                player_stats["losses"],
                player_stats["draws"],
                player_stats["blackjacks"],
                win_rate,
            )
        )

    results.sort(key=lambda x: x[5], reverse=True)

    print(
        f"{'Strategy':<25} {'Wins':<6} {'Losses':<8} {'Draws':<7} {'BJs':<5} {'Win %':<8}"
    )
    print("-" * 70)

    for name, wins, losses, draws, bjs, win_rate in results:
        print(f"{name:<25} {wins:<6} {losses:<8} {draws:<7} {bjs:<5} {win_rate:<8.2f}%")

    print()
    print("=" * 70)
    print("Analysis:")
    print("=" * 70)

    best_strategy = results[0][0]
    best_win_rate = results[0][5]
    print(
        f"Best performing strategy: {best_strategy} with {best_win_rate:.2f}% win rate"
    )

    most_blackjacks = max(results, key=lambda x: x[4])
    print(f"Most blackjacks: {most_blackjacks[0]} with {most_blackjacks[4]} blackjacks")

    print()


if __name__ == "__main__":
    main()
