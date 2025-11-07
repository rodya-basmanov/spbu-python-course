from project.Task4.player import Player, Dealer
from project.Task4.card import Deck


class BlackjackGame:
    def __init__(self, players, rounds=5):
        """
        Create a new game.

        Args:
            players: List of players
            rounds: Number of rounds to play
        """
        self.players = players
        self.dealer = Dealer()
        self.deck = Deck()
        self.rounds = rounds

    def deal(self):
        """Deal 2 cards to each player and dealer."""
        for p in self.players:
            p.add_card(self.deck.draw())
        self.dealer.add_card(self.deck.draw())
        for p in self.players:
            p.add_card(self.deck.draw())
        self.dealer.add_card(self.deck.draw())

    def play_round(self):
        """
        Play one round of blackjack.

        Steps:
        1. Reset all hands
        2. Deal initial cards
        3. Players take their turns
        4. Dealer takes turn if needed
        """
        for p in self.players:
            p.reset()
        self.dealer.reset()

        self.deal()

        for p in self.players:
            while p.should_hit() and not p.hand.is_busted():
                p.add_card(self.deck.draw())

        if any(not p.hand.is_busted() for p in self.players):
            while self.dealer.should_hit() and not self.dealer.hand.is_busted():
                self.dealer.add_card(self.deck.draw())

    def show_results(self):
        """Display results of the round."""
        print(f"Dealer: {self.dealer}")
        for p in self.players:
            print(p)

    def play(self):
        """
        Play the full game for all rounds.

        Plays the specified number of rounds and shows
        results after each round.
        """
        for i in range(self.rounds):
            print(f"\nRound {i+1}:")
            self.play_round()
            self.show_results()


if __name__ == "__main__":
    from project.Task4.strategy import (
        ConservativeStrategy,
        AggressiveStrategy,
        DealerStrategy,
    )

    players = [
        Player("Bot1", ConservativeStrategy()),
        Player("Bot2", AggressiveStrategy()),
        Player("Bot3", DealerStrategy()),
    ]

    game = BlackjackGame(players, rounds=3)
    game.play()
