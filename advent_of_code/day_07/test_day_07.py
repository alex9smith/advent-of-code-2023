from pytest import raises, fixture
from collections import Counter
from day_07 import Card, Hand, Type, total_winnings
from typing import List

INPUT = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""


class TestCard:
    def test_from_char(self):
        assert Card.from_char("K") == Card.KING
        assert Card.from_char("5") == Card.FIVE

        with raises(ValueError):
            Card.from_char("1")


class TestHand:
    @fixture
    def hands(self) -> List[Hand]:
        lines = [
            line
            for line in INPUT.split("\n")
            if not (line == "\n" or line.isspace() or len(line) == 0)
        ]
        return [Hand.from_line(line) for line in lines]

    def test_from_line(self, hands: List[Hand]):
        expected_cards = [Card.THREE, Card.TWO, Card.TEN, Card.THREE, Card.KING]

        assert hands[0] == Hand(
            cards=expected_cards, bid=765, card_counts=Counter(expected_cards)
        )

    def test_type(self, hands: List[Hand]):
        assert hands[0].type == Type.PAIR
        assert hands[1].type == Type.THREE_OF_A_KIND
        assert hands[2].type == Type.TWO_PAIR
        assert hands[3].type == Type.TWO_PAIR
        assert hands[4].type == Type.THREE_OF_A_KIND

    def test_comparison(self, hands: List[Hand]):
        # different types
        assert hands[1] > hands[0]
        assert hands[1] > hands[2]
        assert hands[2] > hands[0]

        # same type
        assert hands[2] > hands[3]
        assert hands[4] > hands[1]


def test_total_winnings():
    lines = [
        line
        for line in INPUT.split("\n")
        if not (line == "\n" or line.isspace() or len(line) == 0)
    ]
    game = [Hand.from_line(line) for line in lines]
    assert total_winnings(game) == 6440
