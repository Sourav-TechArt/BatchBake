from dataclasses import dataclass
from math import floor


@dataclass
class GridCell:
    """
    Represents one grid chunk.

    Example:
        A1
        A2
        B3
    """

    row: int
    col: int

    min_x: float
    max_x: float

    min_y: float
    max_y: float

    @property
    def center(self):
        return (
            (self.min_x + self.max_x) * 0.5,
            (self.min_y + self.max_y) * 0.5,
        )

    @property
    def width(self):
        return self.max_x - self.min_x

    @property
    def height(self):
        return self.max_y - self.min_y

    @property
    def label(self):
        """
        Converts row/column into A1, A2, B3...
        """
        letters = ""

        row = self.row

        while True:
            letters = chr(ord("A") + (row % 26)) + letters
            row = row // 26 - 1

            if row < 0:
                break

        return f"{letters}{self.col + 1}"