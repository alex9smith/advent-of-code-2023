from dataclasses import dataclass
from collections import Counter
from enum import Enum, IntEnum
from typing import List


class Card(IntEnum):
    JOKER = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

    @classmethod
    def from_char(cls, char: str) -> "Card":
        match char:
            case "2":
                return Card.TWO
            case "3":
                return Card.THREE
            case "4":
                return Card.FOUR
            case "5":
                return Card.FIVE
            case "6":
                return Card.SIX
            case "7":
                return Card.SEVEN
            case "8":
                return Card.EIGHT
            case "9":
                return Card.NINE
            case "T":
                return Card.TEN
            case "Q":
                return Card.QUEEN
            case "K":
                return Card.KING
            case "A":
                return Card.ACE
            case "J":
                return Card.JOKER
            case _:
                raise ValueError(f"Couldn't parse char {char}")


class Type(IntEnum):
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7


@dataclass(frozen=True)
class CardCount:
    card: Card
    count: int


@dataclass
class Hand:
    cards: List[Card]
    bid: int
    card_counts: Counter[Card]

    @classmethod
    def from_line(cls, line: str) -> "Hand":
        cards, bid = line.split(" ")
        cards = [Card.from_char(c) for c in cards]
        return Hand(cards=cards, bid=int(bid), card_counts=Counter(cards))

    @property
    def most_common(self) -> CardCount:
        highest_count = max(self.card_counts.values())
        cards_with_highest_count = []

        for card, count in self.card_counts.items():
            if count == highest_count:
                cards_with_highest_count.append(card)

        return CardCount(card=max(cards_with_highest_count), count=highest_count)

    @property
    def most_common_high_card_not_joker(self) -> CardCount:
        if not self.most_common.card == Card.JOKER:
            # If it's already not a Joker
            return self.most_common

        elif self.most_common.count == 5:
            # If it's all jokers
            return self.most_common
        else:
            not_jokers = [card for card in self.cards if not card == Card.JOKER]
            not_jokers_count = Counter(not_jokers)

            highest_count = max(not_jokers_count.values())
            cards_with_highest_count = []

            for card, count in not_jokers_count.items():
                if count == highest_count:
                    cards_with_highest_count.append(card)

            return CardCount(card=max(cards_with_highest_count), count=highest_count)

    @property
    def type(self) -> Type:
        cards_joker_replaced: List[Card] = []
        for card in self.cards:
            if card == Card.JOKER:
                cards_joker_replaced.append(self.most_common_high_card_not_joker.card)
            else:
                cards_joker_replaced.append(card)

        counts_cards_joker_replaced = Counter(cards_joker_replaced)
        match len(counts_cards_joker_replaced):
            case 1:
                return Type.FIVE_OF_A_KIND

            case 2:
                # Either 4 of a kind or full house
                if (
                    counts_cards_joker_replaced.get(
                        self.most_common_high_card_not_joker.card
                    )
                    == 4
                ):
                    return Type.FOUR_OF_A_KIND
                else:
                    return Type.FULL_HOUSE

            case 3:
                # Either 3 of a kind or two pairs
                if (
                    counts_cards_joker_replaced.get(
                        self.most_common_high_card_not_joker.card
                    )
                    == 3
                ):
                    return Type.THREE_OF_A_KIND
                else:
                    return Type.TWO_PAIR

            case 4:
                return Type.PAIR

            case 5:
                return Type.HIGH_CARD

            case _:
                raise ValueError(f"Couldn't calculate type for cards {self.cards}")

    def __lt__(self, other: "Hand") -> bool:
        if self.type < other.type:
            return True

        elif self.type > other.type:
            return False

        else:
            for card, other_card in zip(self.cards, other.cards):
                if card == other_card:
                    continue
                else:
                    return card < other_card
        return False


type Game = List[Hand]


def total_winnings(game: Game) -> int:
    winnings = 0
    game.sort()
    players = len(game)
    for i, hand in enumerate(game[::-1]):
        rank = players - i
        winnings += hand.bid * rank

    return winnings


if __name__ == "__main__":
    with open("./advent_of_code/day_07/day_07.txt", "r") as file:
        lines = [
            line
            for line in file.readlines()
            if not (line == "\n" or line.isspace() or len(line) == 0)
        ]

    game = [Hand.from_line(line) for line in lines]
    print("part 2")
    print(total_winnings(game))
