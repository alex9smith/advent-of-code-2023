from typing import List

type FibonacciSequence = List[int]


def fibonacci(first: int, second: int, terms: int) -> FibonacciSequence:
    if first >= second:
        raise ValueError("second must be greater than first")

    if terms <= 0:
        raise ValueError("terms must be a positive integer")

    if terms == 1:
        return [first]

    elif terms == 2:
        return [first, second]

    else:
        sequence = [first, second]
        x, y = first, second
        while len(sequence) < terms:
            z = x + y
            sequence.append(z)
            x = y
            y = z

        return sequence


if __name__ == "__main__":
    print("\n".join([str(i) for i in fibonacci(1, 2, 5)]))
