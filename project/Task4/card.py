from random import shuffle
from enum import Enum


class Suit(Enum):
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"
    SPADES = "♠"


class Rank(Enum):
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

    def __init__(self, symbol, value):
        self._symbol = symbol
        self._value = value

    @property
    def symbol(self):
        return self._symbol

    @property
    def value(self):
        return self._value


class Card:
    def __init__(self, rank: Rank, suit: Suit):
        """
        Create a card.

        Args:
            rank: Card rank
            suit: Card suit
        """
        self.rank = rank
        self.suit = suit

    @property
    def value(self) -> int:
        """Get card value."""
        return self.rank.value

    def __str__(self) -> str:
        return f"{self.rank.symbol}{self.suit.value}"


class Deck:
    def __init__(self):
        """Create and shuffle a new deck."""
        self.cards = []
        self.reset()

    def reset(self):
        """Create new deck with all 52 cards and shuffle."""
        self.cards = []
        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(rank, suit))
        shuffle(self.cards)

    def draw(self):
        """
        Draw a card from the deck.

        Returns:
            Card from the deck
        """
        if len(self.cards) < 10:
            self.reset()
        return self.cards.pop()
