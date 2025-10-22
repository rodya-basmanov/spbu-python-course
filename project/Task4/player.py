from project.Task4.hand import Hand
from project.Task4.card import Card
from project.Task4.strategy import Strategy, DealerStrategy


class Player:
    """Represents a player in the Blackjack game."""

    def __init__(self, name: str, strategy: Strategy):
        """
        Initialize a player.

        Args:
            name: Player's name
            strategy: Strategy the player will use
        """
        self.name = name
        self.strategy = strategy
        self.hand = Hand()
        self.is_active = True

    def receive_card(self, card: Card) -> None:
        """
        Receive a card and add it to hand.

        Args:
            card: Card to receive
        """
        self.hand.add_card(card)

    def should_hit(self, dealer_upcard: Card) -> bool:
        """
        Decide whether to hit based on strategy.

        Args:
            dealer_upcard: Dealer's visible card

        Returns:
            True if should hit, False if should stand
        """
        if not self.is_active or self.hand.is_busted():
            return False
        return self.strategy.should_hit(self.hand, dealer_upcard)

    def reset_hand(self) -> None:
        """Reset the player's hand for a new round."""
        self.hand.clear()
        self.is_active = True

    def get_hand_value(self) -> int:
        """Get the current value of the player's hand."""
        return self.hand.get_value()

    def is_busted(self) -> bool:
        """Check if the player is busted."""
        return self.hand.is_busted()

    def has_blackjack(self) -> bool:
        """Check if the player has blackjack."""
        return self.hand.is_blackjack()

    def stand(self) -> None:
        """Player chooses to stand."""
        self.is_active = False

    def __str__(self) -> str:
        """String representation of the player."""
        status = (
            "BUSTED" if self.is_busted() else "ACTIVE" if self.is_active else "STAND"
        )
        return f"{self.name} ({self.strategy.get_name()}): {self.hand} [{status}]"

    def __repr__(self) -> str:
        """Detailed representation of the player."""
        return f"Player(name={self.name}, strategy={self.strategy.get_name()}, hand={repr(self.hand)})"


class Dealer:
    """Represents the dealer in the Blackjack game."""

    def __init__(self):
        """Initialize the dealer."""
        self.hand = Hand()
        self.strategy = DealerStrategy()

    def receive_card(self, card: Card) -> None:
        """
        Receive a card and add it to hand.

        Args:
            card: Card to receive
        """
        self.hand.add_card(card)

    def should_hit(self) -> bool:
        """
        Decide whether to hit based on dealer strategy.

        Returns:
            True if should hit, False if should stand
        """
        if self.hand.is_busted():
            return False
        return self.strategy.should_hit(self.hand, self.hand.cards[0])

    def get_upcard(self) -> Card:
        """
        Get the dealer's visible card (first card).

        Returns:
            The dealer's upcard

        Raises:
            IndexError: If dealer has no cards
        """
        if not self.hand.cards:
            raise IndexError("Dealer has no cards")
        return self.hand.cards[0]

    def get_hand_value(self) -> int:
        """Get the current value of the dealer's hand."""
        return self.hand.get_value()

    def is_busted(self) -> bool:
        """Check if the dealer is busted."""
        return self.hand.is_busted()

    def has_blackjack(self) -> bool:
        """Check if the dealer has blackjack."""
        return self.hand.is_blackjack()

    def reset_hand(self) -> None:
        """Reset the dealer's hand for a new round."""
        self.hand.clear()

    def show_upcard(self) -> str:
        """Show only the dealer's upcard (for initial display)."""
        if not self.hand.cards:
            return "Dealer: No cards"
        return f"Dealer: [{self.hand.cards[0]}, ??]"

    def __str__(self) -> str:
        """String representation of the dealer."""
        status = "BUSTED" if self.is_busted() else "PLAYING"
        return f"Dealer: {self.hand} [{status}]"

    def __repr__(self) -> str:
        """Detailed representation of the dealer."""
        return f"Dealer(hand={repr(self.hand)})"
