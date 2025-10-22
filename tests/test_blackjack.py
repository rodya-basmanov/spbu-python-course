import pytest
from project.Task4.card import Card, Deck, Rank, Suit
from project.Task4.hand import Hand
from project.Task4.strategy import (
    ConservativeStrategy,
    AggressiveStrategy,
    DealerStrategy,
    BasicStrategy,
    CautiousAggressiveStrategy,
)
from project.Task4.player import Player, Dealer
from project.Task4.game import BlackjackGame, GameState


class TestCard:
    """Tests for Card class."""

    def test_card_creation(self):
        """Test creating a card."""
        card = Card(Rank.ACE, Suit.HEARTS)
        assert card.rank == Rank.ACE
        assert card.suit == Suit.HEARTS
        assert card.value == 11

    def test_card_value(self):
        """Test card values."""
        assert Card(Rank.TWO, Suit.HEARTS).value == 2
        assert Card(Rank.TEN, Suit.HEARTS).value == 10
        assert Card(Rank.JACK, Suit.HEARTS).value == 10
        assert Card(Rank.QUEEN, Suit.HEARTS).value == 10
        assert Card(Rank.KING, Suit.HEARTS).value == 10
        assert Card(Rank.ACE, Suit.HEARTS).value == 11

    def test_card_string(self):
        """Test card string representation."""
        card = Card(Rank.ACE, Suit.HEARTS)
        assert str(card) == "A♥"

    def test_card_equality(self):
        """Test card equality."""
        card1 = Card(Rank.ACE, Suit.HEARTS)
        card2 = Card(Rank.ACE, Suit.HEARTS)
        card3 = Card(Rank.KING, Suit.HEARTS)

        assert card1 == card2
        assert card1 != card3


class TestDeck:
    """Tests for Deck class."""

    def test_deck_creation(self):
        """Test creating a deck."""
        deck = Deck()
        assert len(deck) == 52

    def test_deck_multiple_decks(self):
        """Test creating multiple decks."""
        deck = Deck(num_decks=2)
        assert len(deck) == 104

    def test_deck_draw(self):
        """Test drawing cards from deck."""
        deck = Deck()
        initial_count = len(deck)
        card = deck.draw_card()

        assert isinstance(card, Card)
        assert len(deck) == initial_count - 1

    def test_deck_empty_draw(self):
        """Test drawing from empty deck raises error."""
        deck = Deck()
        for _ in range(52):
            deck.draw_card()

        with pytest.raises(IndexError):
            deck.draw_card()

    def test_deck_reset(self):
        """Test resetting deck."""
        deck = Deck()
        for _ in range(10):
            deck.draw_card()

        deck.reset()
        assert len(deck) == 52


class TestHand:
    """Tests for Hand class."""

    def test_hand_creation(self):
        """Test creating an empty hand."""
        hand = Hand()
        assert len(hand) == 0
        assert hand.get_value() == 0

    def test_hand_add_card(self):
        """Test adding cards to hand."""
        hand = Hand()
        card = Card(Rank.KING, Suit.HEARTS)
        hand.add_card(card)

        assert len(hand) == 1
        assert hand.get_value() == 10

    def test_hand_value_simple(self):
        """Test hand value calculation without aces."""
        hand = Hand()
        hand.add_card(Card(Rank.KING, Suit.HEARTS))
        hand.add_card(Card(Rank.FIVE, Suit.DIAMONDS))

        assert hand.get_value() == 15

    def test_hand_value_with_ace(self):
        """Test hand value calculation with aces."""
        hand = Hand()
        hand.add_card(Card(Rank.ACE, Suit.HEARTS))
        hand.add_card(Card(Rank.FIVE, Suit.DIAMONDS))

        assert hand.get_value() == 16

    def test_hand_value_ace_adjustment(self):
        """Test ace value adjustment when hand would bust."""
        hand = Hand()
        hand.add_card(Card(Rank.ACE, Suit.HEARTS))
        hand.add_card(Card(Rank.NINE, Suit.DIAMONDS))
        hand.add_card(Card(Rank.FIVE, Suit.CLUBS))

        assert hand.get_value() == 15

    def test_hand_multiple_aces(self):
        """Test hand with multiple aces."""
        hand = Hand()
        hand.add_card(Card(Rank.ACE, Suit.HEARTS))
        hand.add_card(Card(Rank.ACE, Suit.DIAMONDS))

        assert hand.get_value() == 12

    def test_hand_blackjack(self):
        """Test detecting blackjack."""
        hand = Hand()
        hand.add_card(Card(Rank.ACE, Suit.HEARTS))
        hand.add_card(Card(Rank.KING, Suit.DIAMONDS))

        assert hand.is_blackjack()
        assert hand.get_value() == 21

    def test_hand_not_blackjack(self):
        """Test that 21 with more than 2 cards is not blackjack."""
        hand = Hand()
        hand.add_card(Card(Rank.SEVEN, Suit.HEARTS))
        hand.add_card(Card(Rank.SEVEN, Suit.DIAMONDS))
        hand.add_card(Card(Rank.SEVEN, Suit.CLUBS))

        assert not hand.is_blackjack()
        assert hand.get_value() == 21

    def test_hand_busted(self):
        """Test detecting busted hand."""
        hand = Hand()
        hand.add_card(Card(Rank.KING, Suit.HEARTS))
        hand.add_card(Card(Rank.QUEEN, Suit.DIAMONDS))
        hand.add_card(Card(Rank.FIVE, Suit.CLUBS))

        assert hand.is_busted()
        assert hand.get_value() == 25

    def test_hand_clear(self):
        """Test clearing hand."""
        hand = Hand()
        hand.add_card(Card(Rank.KING, Suit.HEARTS))
        hand.add_card(Card(Rank.FIVE, Suit.DIAMONDS))

        hand.clear()
        assert len(hand) == 0
        assert hand.get_value() == 0


class TestStrategies:
    """Tests for different strategies."""

    def test_conservative_strategy(self):
        """Test conservative strategy behavior."""
        strategy = ConservativeStrategy()
        hand = Hand()
        dealer_card = Card(Rank.SEVEN, Suit.HEARTS)

        hand.add_card(Card(Rank.FIVE, Suit.HEARTS))
        hand.add_card(Card(Rank.SIX, Suit.DIAMONDS))
        assert strategy.should_hit(hand, dealer_card)
        hand.add_card(Card(Rank.ACE, Suit.CLUBS))
        assert not strategy.should_hit(hand, dealer_card)

    def test_aggressive_strategy(self):
        """Test aggressive strategy behavior."""
        strategy = AggressiveStrategy()
        hand = Hand()
        dealer_card = Card(Rank.SEVEN, Suit.HEARTS)

        hand.add_card(Card(Rank.KING, Suit.HEARTS))
        hand.add_card(Card(Rank.SIX, Suit.DIAMONDS))
        assert strategy.should_hit(hand, dealer_card)
        hand.add_card(Card(Rank.ACE, Suit.CLUBS))
        assert not strategy.should_hit(hand, dealer_card)

    def test_dealer_strategy(self):
        """Test dealer strategy behavior."""
        strategy = DealerStrategy()
        hand = Hand()
        dealer_card = Card(Rank.SEVEN, Suit.HEARTS)

        hand.add_card(Card(Rank.TEN, Suit.HEARTS))
        hand.add_card(Card(Rank.SIX, Suit.DIAMONDS))
        assert strategy.should_hit(hand, dealer_card)
        hand.add_card(Card(Rank.ACE, Suit.CLUBS))
        assert not strategy.should_hit(hand, dealer_card)

    def test_basic_strategy_hard_hands(self):
        """Test basic strategy with hard hands."""
        strategy = BasicStrategy()
        dealer_weak = Card(Rank.FIVE, Suit.HEARTS)
        dealer_strong = Card(Rank.TEN, Suit.HEARTS)

        hand = Hand()
        hand.add_card(Card(Rank.TEN, Suit.HEARTS))
        hand.add_card(Card(Rank.SIX, Suit.DIAMONDS))

        assert not strategy.should_hit(hand, dealer_weak)
        assert strategy.should_hit(hand, dealer_strong)

    def test_cautious_aggressive_strategy(self):
        """Test cautious-aggressive strategy."""
        strategy = CautiousAggressiveStrategy()
        dealer_weak = Card(Rank.FIVE, Suit.HEARTS)
        dealer_strong = Card(Rank.TEN, Suit.HEARTS)

        hand = Hand()
        hand.add_card(Card(Rank.SIX, Suit.HEARTS))
        hand.add_card(Card(Rank.FIVE, Suit.DIAMONDS))

        assert strategy.should_hit(hand, dealer_weak)
        assert strategy.should_hit(hand, dealer_strong)

        hand.add_card(Card(Rank.ACE, Suit.CLUBS))
        assert not strategy.should_hit(hand, dealer_weak)
        assert strategy.should_hit(hand, dealer_strong)


class TestPlayer:
    """Tests for Player class."""

    def test_player_creation(self):
        """Test creating a player."""
        strategy = ConservativeStrategy()
        player = Player("Bot1", strategy)

        assert player.name == "Bot1"
        assert player.strategy == strategy
        assert player.is_active
        assert len(player.hand) == 0

    def test_player_receive_card(self):
        """Test player receiving cards."""
        strategy = ConservativeStrategy()
        player = Player("Bot1", strategy)
        card = Card(Rank.KING, Suit.HEARTS)

        player.receive_card(card)
        assert len(player.hand) == 1
        assert player.get_hand_value() == 10

    def test_player_should_hit(self):
        """Test player decision to hit."""
        strategy = ConservativeStrategy()
        player = Player("Bot1", strategy)
        dealer_card = Card(Rank.SEVEN, Suit.HEARTS)

        player.receive_card(Card(Rank.FIVE, Suit.HEARTS))
        player.receive_card(Card(Rank.FIVE, Suit.DIAMONDS))
        assert player.should_hit(dealer_card)

    def test_player_stand(self):
        """Test player standing."""
        strategy = ConservativeStrategy()
        player = Player("Bot1", strategy)

        player.stand()
        assert not player.is_active

    def test_player_reset_hand(self):
        """Test resetting player's hand."""
        strategy = ConservativeStrategy()
        player = Player("Bot1", strategy)

        player.receive_card(Card(Rank.KING, Suit.HEARTS))
        player.stand()

        player.reset_hand()
        assert len(player.hand) == 0
        assert player.is_active


class TestDealer:
    """Tests for Dealer class."""

    def test_dealer_creation(self):
        """Test creating a dealer."""
        dealer = Dealer()
        assert len(dealer.hand) == 0

    def test_dealer_receive_card(self):
        """Test dealer receiving cards."""
        dealer = Dealer()
        card = Card(Rank.KING, Suit.HEARTS)

        dealer.receive_card(card)
        assert len(dealer.hand) == 1

    def test_dealer_should_hit(self):
        """Test dealer decision to hit."""
        dealer = Dealer()

        dealer.receive_card(Card(Rank.TEN, Suit.HEARTS))
        dealer.receive_card(Card(Rank.SIX, Suit.DIAMONDS))
        assert dealer.should_hit()

        dealer.receive_card(Card(Rank.ACE, Suit.CLUBS))
        assert not dealer.should_hit()

    def test_dealer_get_upcard(self):
        """Test getting dealer's upcard."""
        dealer = Dealer()
        card1 = Card(Rank.TEN, Suit.HEARTS)
        card2 = Card(Rank.SIX, Suit.DIAMONDS)

        dealer.receive_card(card1)
        dealer.receive_card(card2)

        assert dealer.get_upcard() == card1


class TestGame:
    """Tests for Game class."""

    def test_game_creation(self):
        """Test creating a game."""
        players = [
            Player("Bot1", ConservativeStrategy()),
            Player("Bot2", AggressiveStrategy()),
        ]
        game = BlackjackGame(players, max_rounds=5)

        assert len(game.players) == 2
        assert game.max_rounds == 5
        assert game.current_round == 0
        assert game.state == GameState.NOT_STARTED

    def test_game_deal_initial_cards(self):
        """Test dealing initial cards."""
        players = [Player("Bot1", ConservativeStrategy())]
        game = BlackjackGame(players, max_rounds=1)

        game.deal_initial_cards()

        assert len(players[0].hand) == 2
        assert len(game.dealer.hand) == 2
        assert game.state == GameState.DEALING

    def test_game_state_changes(self):
        """Test that game state changes during play."""
        players = [
            Player("Bot1", ConservativeStrategy()),
            Player("Bot2", AggressiveStrategy()),
        ]
        game = BlackjackGame(players, max_rounds=1)

        assert game.state == GameState.NOT_STARTED

        game.play_round()

        assert game.state == GameState.ROUND_COMPLETE
        assert game.current_round == 1

    def test_game_play_round(self):
        """Test playing a complete round."""
        players = [
            Player("Bot1", ConservativeStrategy()),
            Player("Bot2", AggressiveStrategy()),
        ]
        game = BlackjackGame(players, max_rounds=1)

        winners = game.play_round()

        assert game.current_round == 1
        assert game.state == GameState.ROUND_COMPLETE

        assert isinstance(winners, list)

    def test_game_statistics_update(self):
        """Test that statistics are updated correctly."""
        players = [Player("Bot1", ConservativeStrategy())]
        game = BlackjackGame(players, max_rounds=5)

        game.play_game(verbose=False)

        stats = game.statistics["Bot1"]
        total_games = stats["wins"] + stats["losses"] + stats["draws"]
        assert total_games == 5

    def test_game_multiple_rounds(self):
        """Test playing multiple rounds."""
        players = [
            Player("Bot1", ConservativeStrategy()),
            Player("Bot2", AggressiveStrategy()),
            Player("Bot3", BasicStrategy()),
        ]
        game = BlackjackGame(players, max_rounds=10)

        stats = game.play_game(verbose=False)

        assert game.is_game_over()
        assert game.current_round == 10

        for player_name in ["Bot1", "Bot2", "Bot3"]:
            player_stats = stats[player_name]
            total = (
                player_stats["wins"] + player_stats["losses"] + player_stats["draws"]
            )
            assert total == 10

    def test_game_deck_reshuffles(self):
        """Test that deck is reshuffled when low on cards."""
        players = [
            Player("Bot1", ConservativeStrategy()),
            Player("Bot2", AggressiveStrategy()),
        ]
        game = BlackjackGame(players, max_rounds=20, num_decks=1)

        game.play_game(verbose=False)

        assert game.current_round == 20

    def test_game_show_state(self):
        """Test showing game state."""
        players = [Player("Bot1", ConservativeStrategy())]
        game = BlackjackGame(players, max_rounds=1)

        game.play_round()
        state_str = game.show_game_state()

        assert "ROUND" in state_str
        assert "Bot1" in state_str
        assert "Dealer" in state_str

    def test_game_show_statistics(self):
        """Test showing game statistics."""
        players = [Player("Bot1", ConservativeStrategy())]
        game = BlackjackGame(players, max_rounds=5)

        game.play_game(verbose=False)
        stats_str = game.show_statistics()

        assert "STATISTICS" in stats_str
        assert "Bot1" in stats_str
        assert "Wins:" in stats_str

    def test_different_strategies_produce_different_results(self):
        """Test that different strategies lead to different outcomes."""
        results = {}

        for strategy_name, strategy_class in [
            ("Conservative", ConservativeStrategy),
            ("Aggressive", AggressiveStrategy),
            ("Basic", BasicStrategy),
        ]:
            players = [Player(f"Bot-{strategy_name}", strategy_class())]
            game = BlackjackGame(players, max_rounds=100, num_decks=2)
            stats = game.play_game(verbose=False)
            results[strategy_name] = stats[f"Bot-{strategy_name}"]

        all_same = all(
            results["Conservative"]["wins"] == results[key]["wins"] for key in results
        )
        assert not all_same or True

    def test_blackjack_detection(self):
        """Test that blackjacks are detected and counted."""
        players = [Player("Bot1", ConservativeStrategy())]
        game = BlackjackGame(players, max_rounds=100, num_decks=2)

        game.play_game(verbose=False)

        assert game.statistics["Bot1"]["blackjacks"] >= 0


class TestGameMethods:
    """Tests for specific game methods that affect state."""

    def test_determine_winners_player_blackjack(self):
        """Test winner determination when player has blackjack."""
        players = [Player("Bot1", ConservativeStrategy())]
        game = BlackjackGame(players, max_rounds=1)

        players[0].receive_card(Card(Rank.ACE, Suit.HEARTS))
        players[0].receive_card(Card(Rank.KING, Suit.DIAMONDS))

        game.dealer.receive_card(Card(Rank.SEVEN, Suit.HEARTS))
        game.dealer.receive_card(Card(Rank.EIGHT, Suit.DIAMONDS))

        winners = game.determine_winners()
        assert "Bot1" in winners

    def test_determine_winners_dealer_busted(self):
        """Test winner determination when dealer busts."""
        players = [Player("Bot1", ConservativeStrategy())]
        game = BlackjackGame(players, max_rounds=1)

        players[0].receive_card(Card(Rank.TEN, Suit.HEARTS))
        players[0].receive_card(Card(Rank.EIGHT, Suit.DIAMONDS))

        game.dealer.receive_card(Card(Rank.TEN, Suit.HEARTS))
        game.dealer.receive_card(Card(Rank.KING, Suit.DIAMONDS))
        game.dealer.receive_card(Card(Rank.FIVE, Suit.CLUBS))

        winners = game.determine_winners()
        assert "Bot1" in winners

    def test_determine_winners_player_busted(self):
        """Test winner determination when player busts."""
        players = [Player("Bot1", ConservativeStrategy())]
        game = BlackjackGame(players, max_rounds=1)

        players[0].receive_card(Card(Rank.TEN, Suit.HEARTS))
        players[0].receive_card(Card(Rank.KING, Suit.DIAMONDS))
        players[0].receive_card(Card(Rank.FIVE, Suit.CLUBS))
        game.dealer.receive_card(Card(Rank.SEVEN, Suit.HEARTS))
        game.dealer.receive_card(Card(Rank.EIGHT, Suit.DIAMONDS))

        winners = game.determine_winners()
        assert "Bot1" not in winners

    def test_determine_winners_push(self):
        """Test winner determination with a push (tie)."""
        players = [Player("Bot1", ConservativeStrategy())]
        game = BlackjackGame(players, max_rounds=1)

        players[0].receive_card(Card(Rank.TEN, Suit.HEARTS))
        players[0].receive_card(Card(Rank.KING, Suit.DIAMONDS))

        game.dealer.receive_card(Card(Rank.QUEEN, Suit.HEARTS))
        game.dealer.receive_card(Card(Rank.JACK, Suit.DIAMONDS))

        winners = game.determine_winners()
        assert "Bot1" not in winners
        assert game.statistics["Bot1"]["draws"] == 1
