from enum import Enum
from random import shuffle
from typing import List


class Suit(Enum):
    """Card suit enumeration."""

    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"
    SPADES = "♠"


class Rank(Enum):
    """Card rank enumeration."""

    TWO = ("2", 2)
    THREE = ("3", 3)
    FOUR = ("4", 4)
    FIVE = ("5", 5)
    SIX = ("6", 6)
    SEVEN = ("7", 7)
    EIGHT = ("8", 8)
    NINE = ("9", 9)
    TEN = ("10", 10)
    JACK = ("J", 10)
    QUEEN = ("Q", 10)
    KING = ("K", 10)
    ACE = ("A", 11)

    def __init__(self, symbol: str, card_value: int):
        self.symbol = symbol
        self.card_value = card_value


class Card:
    """Represents a single playing card."""

    def __init__(self, rank: Rank, suit: Suit):
        """
        Initialize a card.

        Args:
            rank: Card rank
            suit: Card suit
        """
        self.rank = rank
        self.suit = suit

    @property
    def value(self) -> int:
        """Get the base value of the card."""
        return self.rank.card_value

    def __str__(self) -> str:
        """String representation of the card."""
        return f"{self.rank.symbol}{self.suit.value}"

    def __repr__(self) -> str:
        """Detailed representation of the card."""
        return f"Card({self.rank.name}, {self.suit.name})"

    def __eq__(self, other) -> bool:
        """Check equality with another card."""
        if not isinstance(other, Card):
            return False
        return self.rank == other.rank and self.suit == other.suit


class Deck:
    """Represents a deck of playing cards."""

    def __init__(self, num_decks: int = 1):
        """
        Initialize a deck.

        Args:
            num_decks: Number of standard 52-card decks to use
        """
        self.num_decks = num_decks
        self.cards: List[Card] = []
        self.reset()

    def reset(self) -> None:
        """Reset and shuffle the deck."""
        self.cards = []
        for _ in range(self.num_decks):
            for suit in Suit:
                for rank in Rank:
                    self.cards.append(Card(rank, suit))
        self.shuffle()

    def shuffle(self) -> None:
        """Shuffle the deck."""
        shuffle(self.cards)

    def draw_card(self) -> Card:
        """
        Draw a card from the deck.

        Returns:
            The drawn card

        Raises:
            IndexError: If the deck is empty
        """
        if not self.cards:
            raise IndexError("Cannot draw from empty deck")
        return self.cards.pop()

    def cards_remaining(self) -> int:
        """Get the number of cards remaining in the deck."""
        return len(self.cards)

    def __len__(self) -> int:
        """Get the number of cards in the deck."""
        return len(self.cards)

    def __str__(self) -> str:
        """String representation of the deck."""
        return f"Deck({self.cards_remaining()} cards remaining)"
