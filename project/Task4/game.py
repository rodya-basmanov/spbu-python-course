from enum import Enum
from typing import List, Dict
from project.Task4.card import Deck
from project.Task4.player import Player, Dealer


class GameState(Enum):
    """Enum representing the state of the game."""

    NOT_STARTED = "Not Started"
    DEALING = "Dealing Initial Cards"
    PLAYERS_TURN = "Players' Turn"
    DEALERS_TURN = "Dealer's Turn"
    ROUND_COMPLETE = "Round Complete"
    GAME_OVER = "Game Over"


class BlackjackGame:
    """Main game class for Blackjack."""

    def __init__(self, players: List[Player], max_rounds: int = 10, num_decks: int = 1):
        """
        Initialize the Blackjack game.

        Args:
            players: List of players participating in the game
            max_rounds: Maximum number of rounds to play
            num_decks: Number of decks to use
        """
        self.players = players
        self.dealer = Dealer()
        self.deck = Deck(num_decks)
        self.max_rounds = max_rounds
        self.current_round = 0
        self.state = GameState.NOT_STARTED
        self.round_winners: List[str] = []
        self.statistics: Dict[str, Dict[str, int]] = {
            player.name: {"wins": 0, "losses": 0, "draws": 0, "blackjacks": 0}
            for player in players
        }

    def get_state(self) -> GameState:
        """Get the current game state."""
        return self.state

    def get_current_round(self) -> int:
        """Get the current round number."""
        return self.current_round

    def show_game_state(self) -> str:
        """
        Get a string representation of the current game state.

        Returns:
            Formatted string showing game state
        """
        lines = []
        lines.append("=" * 70)
        lines.append(
            f"ROUND {self.current_round}/{self.max_rounds} - State: {self.state.value}"
        )
        lines.append("=" * 70)

        if self.state in [GameState.DEALING, GameState.PLAYERS_TURN]:
            lines.append(self.dealer.show_upcard())
        else:
            lines.append(str(self.dealer))

        lines.append("-" * 70)

        for player in self.players:
            lines.append(str(player))

        lines.append("=" * 70)
        return "\n".join(lines)

    def show_statistics(self) -> str:
        """
        Get a string representation of game statistics.

        Returns:
            Formatted string showing statistics for all players
        """
        lines = []
        lines.append("=" * 70)
        lines.append("GAME STATISTICS")
        lines.append("=" * 70)

        for player_name, stats in self.statistics.items():
            total_games = stats["wins"] + stats["losses"] + stats["draws"]
            win_rate = (stats["wins"] / total_games * 100) if total_games > 0 else 0
            lines.append(f"{player_name}:")
            lines.append(
                f"  Wins: {stats['wins']}, Losses: {stats['losses']}, "
                f"Draws: {stats['draws']}, Blackjacks: {stats['blackjacks']}"
            )
            lines.append(f"  Win Rate: {win_rate:.1f}%")

        lines.append("=" * 70)
        return "\n".join(lines)

    def deal_initial_cards(self) -> None:
        """Deal initial two cards to each player and the dealer."""
        self.state = GameState.DEALING

        for player in self.players:
            player.receive_card(self.deck.draw_card())

        self.dealer.receive_card(self.deck.draw_card())
        for player in self.players:
            player.receive_card(self.deck.draw_card())

        self.dealer.receive_card(self.deck.draw_card())

    def play_players_turn(self) -> None:
        """Execute the players' turn."""
        self.state = GameState.PLAYERS_TURN

        dealer_upcard = self.dealer.get_upcard()

        for player in self.players:
            if player.has_blackjack():
                self.statistics[player.name]["blackjacks"] += 1
                player.stand()
                continue
            while player.should_hit(dealer_upcard):
                card = self.deck.draw_card()
                player.receive_card(card)

                if player.is_busted():
                    break

            if not player.is_busted() and player.is_active:
                player.stand()

    def play_dealers_turn(self) -> None:
        """Execute the dealer's turn."""
        self.state = GameState.DEALERS_TURN

        any_player_active = any(not player.is_busted() for player in self.players)

        if any_player_active:
            while self.dealer.should_hit():
                card = self.deck.draw_card()
                self.dealer.receive_card(card)

                if self.dealer.is_busted():
                    break

    def determine_winners(self) -> List[str]:
        """
        Determine the winners of the round.

        Returns:
            List of winner names
        """
        winners = []
        dealer_value = self.dealer.get_hand_value()
        dealer_busted = self.dealer.is_busted()
        dealer_blackjack = self.dealer.has_blackjack()

        for player in self.players:
            player_value = player.get_hand_value()
            player_busted = player.is_busted()
            player_blackjack = player.has_blackjack()

            if player_busted:
                self.statistics[player.name]["losses"] += 1
                continue
            if dealer_busted:
                winners.append(player.name)
                self.statistics[player.name]["wins"] += 1
                continue
            if player_blackjack and dealer_blackjack:
                self.statistics[player.name]["draws"] += 1
                continue
            if player_blackjack:
                winners.append(player.name)
                self.statistics[player.name]["wins"] += 1
                continue
            if dealer_blackjack:
                self.statistics[player.name]["losses"] += 1
                continue
            if player_value > dealer_value:
                winners.append(player.name)
                self.statistics[player.name]["wins"] += 1
            elif player_value < dealer_value:
                self.statistics[player.name]["losses"] += 1
            else:
                self.statistics[player.name]["draws"] += 1

        return winners

    def play_round(self) -> List[str]:
        """
        Play a single round of Blackjack.

        Returns:
            List of winner names for the round
        """
        self.current_round += 1

        for player in self.players:
            player.reset_hand()
        self.dealer.reset_hand()
        if self.deck.cards_remaining() < (len(self.players) + 1) * 5:
            self.deck.reset()

        self.deal_initial_cards()

        self.play_players_turn()

        self.play_dealers_turn()

        self.state = GameState.ROUND_COMPLETE
        winners = self.determine_winners()
        self.round_winners = winners

        return winners

    def play_game(self, verbose: bool = True) -> Dict[str, Dict[str, int]]:
        """
        Play the full game for the specified number of rounds.

        Args:
            verbose: Whether to print game state after each round

        Returns:
            Dictionary of statistics for each player
        """
        self.state = GameState.NOT_STARTED

        for round_num in range(self.max_rounds):
            if verbose:
                print(f"\n{'='*70}")
                print(f"Starting Round {round_num + 1}/{self.max_rounds}")
                print(f"{'='*70}\n")

            self.play_round()

            if verbose:
                print(self.show_game_state())

                if self.round_winners:
                    print(f"\n🏆 Winners: {', '.join(self.round_winners)}")
                else:
                    print(f"\n🤝 No winners this round (all players busted or draw)")

        self.state = GameState.GAME_OVER

        if verbose:
            print("\n" + self.show_statistics())

        return self.statistics

    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return (
            self.current_round >= self.max_rounds or self.state == GameState.GAME_OVER
        )


if __name__ == "__main__":
    from project.Task4.strategy import (
        ConservativeStrategy,
        AggressiveStrategy,
        BasicStrategy,
    )

    print("=" * 70)
    print("BLACKJACK GAME")
    print("=" * 70)
    print()

    players = [
        Player("Conservative Bot", ConservativeStrategy()),
        Player("Aggressive Bot", AggressiveStrategy()),
        Player("Basic Strategy Bot", BasicStrategy()),
    ]

    game = BlackjackGame(players, max_rounds=5, num_decks=2)
    game.play_game(verbose=True)
