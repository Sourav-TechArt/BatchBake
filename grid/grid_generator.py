from math import ceil

from .grid_cell import GridCell


class GridGenerator:

    def __init__(
        self,
        min_x,
        min_y,
        max_x,
        max_y,
        chunk_size,
    ):
        self.min_x = min_x
        self.min_y = min_y

        self.max_x = max_x
        self.max_y = max_y

        self.chunk_size = chunk_size

    def generate(self):

        width = self.max_x - self.min_x
        height = self.max_y - self.min_y

        cols = ceil(width / self.chunk_size)
        rows = ceil(height / self.chunk_size)

        cells = []

        for row in range(rows):

            for col in range(cols):

                x0 = self.min_x + col * self.chunk_size
                x1 = min(x0 + self.chunk_size, self.max_x)

                y0 = self.min_y + row * self.chunk_size
                y1 = min(y0 + self.chunk_size, self.max_y)

                cells.append(
                    GridCell(
                        row=row,
                        col=col,
                        min_x=x0,
                        max_x=x1,
                        min_y=y0,
                        max_y=y1,
                    )
                )

        return cells