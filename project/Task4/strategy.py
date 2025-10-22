from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from project.Task4.hand import Hand
    from project.Task4.card import Card


class Strategy(ABC):
    """Abstract base class for player strategies."""

    @abstractmethod
    def should_hit(self, hand: "Hand", dealer_upcard: "Card") -> bool:
        """
        Decide whether to hit or stand.

        Args:
            hand: Player's current hand
            dealer_upcard: Dealer's visible card

        Returns:
            True if should hit, False if should stand
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Get the name of the strategy."""
        pass


class ConservativeStrategy(Strategy):
    """
    Conservative strategy: stands on 12 or higher.

    This strategy is very cautious and tries to avoid busting.
    """

    def should_hit(self, hand: "Hand", dealer_upcard: "Card") -> bool:
        """Stand on 12 or higher to avoid busting."""
        return hand.get_value() < 12

    def get_name(self) -> str:
        """Get strategy name."""
        return "Conservative"


class AggressiveStrategy(Strategy):
    """
    Aggressive strategy: hits until 17 or higher.

    This strategy takes more risks to get closer to 21.
    """

    def should_hit(self, hand: "Hand", dealer_upcard: "Card") -> bool:
        """Hit until 17 or higher."""
        return hand.get_value() < 17

    def get_name(self) -> str:
        """Get strategy name."""
        return "Aggressive"


class DealerStrategy(Strategy):
    """
    Dealer strategy: hits on 16 or less, stands on 17 or more.

    This is the standard dealer strategy used in most casinos.
    """

    def should_hit(self, hand: "Hand", dealer_upcard: "Card") -> bool:
        """Hit on 16 or less, stand on 17 or more."""
        return hand.get_value() < 17

    def get_name(self) -> str:
        """Get strategy name."""
        return "Dealer"


class BasicStrategy(Strategy):
    """
    Basic strategy: follows optimal play based on mathematical calculations.

    This strategy considers both the player's hand and the dealer's upcard
    to make the mathematically optimal decision.
    """

    def should_hit(self, hand: "Hand", dealer_upcard: "Card") -> bool:
        """Make decisions based on basic strategy chart."""
        hand_value = hand.get_value()
        dealer_value = dealer_upcard.value

        if hand_value <= 11:
            return True

        if hand.is_soft():
            if hand_value <= 18:
                return dealer_value >= 9
            return False
        if hand_value >= 17:
            return False
        if hand_value >= 13:
            return dealer_value >= 7
        if hand_value == 12:
            return dealer_value < 4 or dealer_value > 6
        return True

    def get_name(self) -> str:
        """Get strategy name."""
        return "Basic"


class CautiousAggressiveStrategy(Strategy):
    """
    Cautious-Aggressive strategy: adapts based on dealer's upcard.

    More aggressive against weak dealer cards (2-6),
    more conservative against strong dealer cards (7-Ace).
    """

    def should_hit(self, hand: "Hand", dealer_upcard: "Card") -> bool:
        """Adapt strategy based on dealer's upcard."""
        hand_value = hand.get_value()
        dealer_value = dealer_upcard.value

        if 2 <= dealer_value <= 6:
            return hand_value < 12

        return hand_value < 17

    def get_name(self) -> str:
        """Get strategy name."""
        return "Cautious-Aggressive"
