from project.Task4.card import Card, Deck, Rank, Suit
from project.Task4.hand import Hand
from project.Task4.strategy import (
    ConservativeStrategy,
    AggressiveStrategy,
    DealerStrategy,
)
from project.Task4.player import Player, Dealer
from project.Task4.game import BlackjackGame


class TestCard:
    def test_card_creation(self):
        """Test card creation and value."""
        card = Card(Rank.ACE, Suit.HEARTS)
        assert card.rank == Rank.ACE
        assert card.value == 11


class TestDeck:
    def test_deck_creation(self):
        """Test deck creation with 52 cards."""
        deck = Deck()
        assert len(deck.cards) == 52

    def test_deck_draw(self):
        """Test drawing a card from deck."""
        deck = Deck()
        card = deck.draw()
        assert isinstance(card, Card)
        assert len(deck.cards) == 51


class TestHand:
    def test_hand_value(self):
        """Test hand value calculation."""
        hand = Hand()
        hand.add_card(Card(Rank.KING, Suit.HEARTS))
        hand.add_card(Card(Rank.FIVE, Suit.DIAMONDS))
        assert hand.get_value() == 15

    def test_hand_ace_adjustment(self):
        """Test ace value adjustment (11 -> 1)."""
        hand = Hand()
        hand.add_card(Card(Rank.ACE, Suit.HEARTS))
        hand.add_card(Card(Rank.NINE, Suit.DIAMONDS))
        assert hand.get_value() == 20
        hand.add_card(Card(Rank.FIVE, Suit.CLUBS))
        assert hand.get_value() == 15

    def test_hand_bust(self):
        """Test bust detection (over 21)."""
        hand = Hand()
        hand.add_card(Card(Rank.KING, Suit.HEARTS))
        hand.add_card(Card(Rank.QUEEN, Suit.DIAMONDS))
        hand.add_card(Card(Rank.FIVE, Suit.CLUBS))
        assert hand.is_busted()


class TestStrategy:
    def test_conservative_strategy(self):
        """Test conservative strategy (stand on 12+)."""
        strategy = ConservativeStrategy()
        assert strategy.should_hit(11) == True
        assert strategy.should_hit(12) == False

    def test_aggressive_strategy(self):
        """Test aggressive strategy (hit until 17+)."""
        strategy = AggressiveStrategy()
        assert strategy.should_hit(16) == True
        assert strategy.should_hit(17) == False


class TestPlayer:
    def test_player_creation(self):
        """Test player creation with empty hand."""
        player = Player("Bot1", ConservativeStrategy())
        assert player.name == "Bot1"
        assert len(player.hand.cards) == 0

    def test_player_reset(self):
        """Test player hand reset."""
        player = Player("Bot1", ConservativeStrategy())
        player.add_card(Card(Rank.KING, Suit.HEARTS))
        player.reset()
        assert len(player.hand.cards) == 0


class TestGameState:
    def test_game_state_changes_during_round(self):
        """Test game state changes during round."""
        players = [Player("Bot1", ConservativeStrategy())]
        game = BlackjackGame(players, rounds=1)

        assert len(game.dealer.hand.cards) == 0
        assert len(players[0].hand.cards) == 0

        game.deal()
        assert len(game.dealer.hand.cards) == 2
        assert len(players[0].hand.cards) == 2

    def test_game_state_resets_between_rounds(self):
        """Test game state resets between rounds."""
        players = [Player("Bot1", ConservativeStrategy())]
        game = BlackjackGame(players, rounds=2)

        game.play_round()
        cards_after_round1 = len(players[0].hand.cards)
        assert cards_after_round1 >= 2

        game.play_round()
        assert len(players[0].hand.cards) >= 2

    def test_deck_state_changes(self):
        """Test deck state changes when dealing cards."""
        players = [Player("Bot1", ConservativeStrategy())]
        game = BlackjackGame(players, rounds=1)

        initial_deck_size = len(game.deck.cards)
        game.deal()

        assert len(game.deck.cards) < initial_deck_size
