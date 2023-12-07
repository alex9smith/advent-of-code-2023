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

ALTERNATE_INPUT = """
2345A 1
Q2KJJ 13
Q2Q2Q 19
T3T3J 17
T3Q33 11
2345J 3
J345A 2
32T3K 5
T55J5 29
KK677 7
KTJJT 34
QQQJA 31
JJJJJ 37
JAAAA 43
AAAAJ 59
AAAAA 61
2AAAA 23
2JJJJ 53
JJJJ2 41
"""


class TestCard:
    def test_from_char(self):
        assert Card.from_char("K") == Card.KING
        assert Card.from_char("5") == Card.FIVE
        assert Card.from_char("J") == Card.JOKER

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
        assert hands[1].type == Type.FOUR_OF_A_KIND
        assert hands[2].type == Type.TWO_PAIR
        assert hands[3].type == Type.FOUR_OF_A_KIND
        assert hands[4].type == Type.FOUR_OF_A_KIND

        assert Hand.from_line("22JKK 1").type == Type.FULL_HOUSE
        assert Hand.from_line("KKJ22 2").type == Type.FULL_HOUSE

    def test_comparison(self, hands: List[Hand]):
        # Edge cases
        assert Hand.from_line("Q2KJJ 13") > Hand.from_line("T3Q33 11")
        assert Hand.from_line("T3T3J 17") > Hand.from_line("Q2KJJ 13")
        assert Hand.from_line("T55J5 29") > Hand.from_line("2AAAA 23")

        # different types
        assert hands[1] > hands[0]
        assert hands[1] > hands[2]
        assert hands[2] > hands[0]
        assert Hand.from_line("JJJJ4 1") > hands[0]

        # same type
        assert hands[3] > hands[1]
        assert hands[3] > hands[4]
        assert hands[4] > hands[1]

        # full houses
        assert Hand.from_line("KKJ22 2") > Hand.from_line("22JKK 1")

    def test_most_common(self, hands: List[Hand]):
        assert Hand.from_line("22JKK 1").most_common.card == Card.KING
        assert Hand.from_line("JJJJ4 1").most_common.card == Card.JOKER
        assert Hand.from_line("Q2KJJ 13").most_common.card == Card.JOKER

    def test_most_common_high_card_not_joker(self, hands: List[Hand]):
        assert (
            Hand.from_line("22JKK 1").most_common_high_card_not_joker.card == Card.KING
        )

        assert hands[0].most_common_high_card_not_joker.card == Card.THREE
        assert hands[1].most_common_high_card_not_joker.card == Card.FIVE
        assert hands[2].most_common_high_card_not_joker.card == Card.KING
        assert hands[3].most_common_high_card_not_joker.card == Card.TEN
        assert hands[4].most_common_high_card_not_joker.card == Card.QUEEN

        assert (
            Hand.from_line("KKJ22 2").most_common_high_card_not_joker.card == Card.KING
        )
        assert (
            Hand.from_line("22JKK 1").most_common_high_card_not_joker.card == Card.KING
        )
        assert (
            Hand.from_line("JJJJ4 1").most_common_high_card_not_joker.card == Card.FOUR
        )
        assert (
            Hand.from_line("Q2KJJ 13").most_common_high_card_not_joker.card == Card.KING
        )
        assert (
            Hand.from_line("JJJJJ 13").most_common_high_card_not_joker.card
            == Card.JOKER
        )
        assert (
            Hand.from_line("23456 13").most_common_high_card_not_joker.card == Card.SIX
        )


def test_total_winnings():
    # lines = [
    #     line
    #     for line in INPUT.split("\n")
    #     if not (line == "\n" or line.isspace() or len(line) == 0)
    # ]
    # game = [Hand.from_line(line) for line in lines]
    # assert total_winnings(game) == 5905

    alternate_lines = [
        line
        for line in ALTERNATE_INPUT.split("\n")
        if not (line == "\n" or line.isspace() or len(line) == 0)
    ]
    alternate_game = [Hand.from_line(line) for line in alternate_lines]
    assert total_winnings(alternate_game) == 6839
