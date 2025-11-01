from project.Task4.hand import Hand
from project.Task4.card import Card
from project.Task4.strategy import Strategy, DealerStrategy


class Player:
    def __init__(self, name: str, strategy: Strategy):
        """
        Create a player.

        Args:
            name: Player name
            strategy: Strategy to use for decisions
        """
        self.name = name
        self.strategy = strategy
        self.hand = Hand()

    def add_card(self, card: Card):
        """
        Add a card to player's hand.

        Args:
            card: Card to add
        """
        self.hand.add(card)

    def should_hit(self) -> bool:
        """
        Decide if player should take another card.

        Returns:
            True if should hit, False if should stand
        """
        return self.strategy.should_hit(self.hand.get_value())

    def reset(self):
        """Clear hand for new round."""
        self.hand.clear()

    def __str__(self) -> str:
        return f"{self.name}: {self.hand}"


class Dealer:
    def __init__(self):
        """Create a dealer with dealer strategy."""
        self.hand = Hand()
        self.strategy = DealerStrategy()

    def add_card(self, card: Card):
        """
        Add a card to dealer's hand.

        Args:
            card: Card to add
        """
        self.hand.add(card)

    def should_hit(self) -> bool:
        """
        Decide if dealer should take another card.

        Returns:
            True if should hit, False if should stand
        """
        return self.strategy.should_hit(self.hand.get_value())

    def reset(self):
        """Clear hand for new round."""
        self.hand.clear()

    def show_first_card(self) -> str:
        """
        Show only the first card (for initial display).

        Returns:
            String showing first card and hiding others
        """
        if self.hand.cards:
            return f"Dealer: {self.hand.cards[0]} [?]"
        return "Dealer: []"

    def __str__(self) -> str:
        return f"Dealer: {self.hand}"
