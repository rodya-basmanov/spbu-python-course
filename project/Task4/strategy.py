class Strategy:
    def should_hit(self, hand_value: int) -> bool:
        """
        Decide if should take another card.

        Args:
            hand_value: Current hand value

        Returns:
            True if should hit, False if should stand
        """
        pass

    def get_name(self) -> str:
        """
        Get strategy name.

        Returns:
            Name of the strategy
        """
        pass


class ConservativeStrategy(Strategy):
    def should_hit(self, hand_value: int) -> bool:
        """
        Hit if hand value is less than 12.

        Args:
            hand_value: Current hand value

        Returns:
            True if should hit, False if should stand
        """
        return hand_value < 12

    def get_name(self) -> str:
        """Get strategy name."""
        return "Conservative"


class AggressiveStrategy(Strategy):
    def should_hit(self, hand_value: int) -> bool:
        """
        Hit if hand value is less than 17.

        Args:
            hand_value: Current hand value

        Returns:
            True if should hit, False if should stand
        """
        return hand_value < 17

    def get_name(self) -> str:
        """Get strategy name."""
        return "Aggressive"


class DealerStrategy(Strategy):
    def should_hit(self, hand_value: int) -> bool:
        """
        Hit if hand value is less than 17 (standard dealer rule).

        Args:
            hand_value: Current hand value

        Returns:
            True if should hit, False if should stand
        """
        return hand_value < 17

    def get_name(self) -> str:
        """Get strategy name."""
        return "Dealer"
