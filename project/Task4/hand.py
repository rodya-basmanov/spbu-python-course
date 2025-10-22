from typing import List
from project.Task4.card import Card, Rank


class Hand:
    """Represents a hand of cards in Blackjack."""

    def __init__(self):
        """Initialize an empty hand."""
        self.cards: List[Card] = []

    def add_card(self, card: Card) -> None:
        """
        Add a card to the hand.

        Args:
            card: Card to add
        """
        self.cards.append(card)

    def get_value(self) -> int:
        """
        Calculate the best value of the hand.

        Aces are counted as 11 or 1, whichever is better.

        Returns:
            The best value of the hand
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

    def is_busted(self) -> bool:
        """Check if the hand is busted (value > 21)."""
        return self.get_value() > 21

    def is_blackjack(self) -> bool:
        """Check if the hand is a natural blackjack (21 with 2 cards)."""
        return len(self.cards) == 2 and self.get_value() == 21

    def is_soft(self) -> bool:
        """
        Check if the hand is soft (contains an ace counted as 11).

        Returns:
            True if the hand contains an ace counted as 11
        """
        value = sum(card.value for card in self.cards)
        aces = sum(1 for card in self.cards if card.rank == Rank.ACE)

        return aces > 0 and value > 21 and not self.is_busted()

    def clear(self) -> None:
        """Clear all cards from the hand."""
        self.cards = []

    def __len__(self) -> int:
        """Get the number of cards in the hand."""
        return len(self.cards)

    def __str__(self) -> str:
        """String representation of the hand."""
        cards_str = ", ".join(str(card) for card in self.cards)
        return f"[{cards_str}] (value: {self.get_value()})"

    def __repr__(self) -> str:
        """Detailed representation of the hand."""
        return f"Hand({len(self.cards)} cards, value={self.get_value()})"
