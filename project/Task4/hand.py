from typing import List
from project.Task4.card import Card, Rank


class Hand:
    def __init__(self):
        """Create an empty hand."""
        self.cards: List[Card] = []

    def add_card(self, card: Card):
        """
        Add a card to the hand.

        Args:
            card: Card to add
        """
        self.cards.append(card)

    def add(self, card: Card):
        """
        Add a card to the hand (alias).

        Args:
            card: Card to add
        """
        self.add_card(card)

    def clear(self):
        """Remove all cards from the hand."""
        self.cards = []

    def get_value(self):
        """
        Calculate the value of the hand.
        Aces are counted as 11 or 1 to avoid busting.

        Returns:
            Total value of the hand
        """
        value = 0
        aces = 0

        for card in self.cards:
            value += card.value
            if card.rank == Rank.ACE:
                aces += 1
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1

        return value

    def is_busted(self):
        """
        Check if hand is busted (over 21).

        Returns:
            True if busted, False otherwise
        """
        return self.get_value() > 21

    def is_blackjack(self) -> bool:
        """
        Check if hand is blackjack (21 with 2 cards).

        Returns:
            True if blackjack, False otherwise
        """
        return len(self.cards) == 2 and self.get_value() == 21

    def __str__(self):
        cards_str = ", ".join(str(card) for card in self.cards)
        return f"[{cards_str}] (value: {self.get_value()})"
