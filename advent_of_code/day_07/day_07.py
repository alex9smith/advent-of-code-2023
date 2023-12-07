from dataclasses import dataclass
from collections import Counter
from enum import Enum
from typing import List


class Card(Enum):
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

    def __lt__(self, other: "Card") -> bool:
        return self.value < other.value

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
            case "J":
                return Card.JACK
            case "Q":
                return Card.QUEEN
            case "K":
                return Card.KING
            case "A":
                return Card.ACE
            case _:
                raise ValueError(f"Couldn't parse char {char}")


class Type(Enum):
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7

    def __lt__(self, other: "Type") -> bool:
        return self.value < other.value


@dataclass
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
        most_common = self.card_counts.most_common(1)[0]
        return CardCount(most_common[0], most_common[1])

    @property
    def type(self) -> Type:
        match len(self.card_counts):
            case 1:
                return Type.FIVE_OF_A_KIND

            case 2:
                # Either 4 of a kind or full house
                if self.most_common.count == 4:
                    return Type.FOUR_OF_A_KIND
                else:
                    return Type.FULL_HOUSE

            case 3:
                # Either 3 of a kind or two pairs
                if self.most_common.count == 3:
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
    print("part 1")
    print(total_winnings(game))
