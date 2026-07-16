import sys

PROJECT_PATH = r"C:\Users\ASUS\Downloads\GeoBake\BatchBake"

if PROJECT_PATH not in sys.path:
    sys.path.append(PROJECT_PATH)

from grid.grid_manager import GridManager
from pipeline.pipeline import Pipeline


def main():

    # --------------------------------------------
    # Generate Test Grid
    # --------------------------------------------

    manager = GridManager()

    manager.generate(
        min_x=0,
        min_y=0,
        max_x=2500,
        max_y=2500,
        chunk_size=500,
        draw_labels=True,
        label_size=40,
        label_height=2,
    )

    manager.print_summary()

    # --------------------------------------------
    # Process ONLY first chunk
    # --------------------------------------------

    first_cell = manager.cells[0]

    print("\n================================")
    print(f"Testing Chunk : {first_cell.label}")
    print("================================")

    pipeline = Pipeline()

    pipeline.process(first_cell)


if __name__ == "__main__":
    main()