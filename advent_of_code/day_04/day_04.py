from dataclasses import dataclass
from tkinter import N
from typing import Set, List


@dataclass
class Card:
    id: int
    numbers: Set[int]
    winners: Set[int]

    @classmethod
    def from_line(cls, line: str) -> "Card":
        prefix, data = line.split(":")

        card_id = prefix.replace("Card", "").strip()
        numbers, winners = data.split("|")

        numbers = set([int(n) for n in numbers.split() if not n.isspace()])
        winners = set([int(w) for w in winners.split() if not w.isspace()])

        return Card(id=int(card_id), numbers=numbers, winners=winners)

    def score(self) -> int:
        num_winners = len(self.numbers.intersection(self.winners))
        if num_winners == 0:
            return 0
        else:
            return pow(2, (num_winners - 1))


def sum_card_scores(lines: list[str]) -> int:
    cards = [Card.from_line(line) for line in lines]
    return sum([card.score() for card in cards])


if __name__ == "__main__":
    with open("./advent_of_code/day_04/day_04.txt", "r") as file:
        lines = [line.strip() for line in file.readlines()]

    print("part 1")
    print(sum_card_scores(lines))
