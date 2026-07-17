import sys
import bpy

PROJECT_PATH = r"E:\Work\MAP_Rnd\GeoBake\BatchBake"

if PROJECT_PATH not in sys.path:
    sys.path.append(PROJECT_PATH)

from grid.grid_manager import GridManager
from pipeline.pipeline import Pipeline

PLATEAU_OBJECT = "PLATEAU"
BING_OBJECT = "BING"

def main():

    # --------------------------------------------------
    # User Settings
    # --------------------------------------------------

    OUTPUT_FOLDER = r"E:\GeoBake_Output"

    CHUNK_SIZE = 500

    CITY_MIN_X = 0
    CITY_MIN_Y = 0

    CITY_MAX_X = 2500
    CITY_MAX_Y = 2500

    LABEL_SIZE = 40
    LABEL_HEIGHT = 2

    # --------------------------------------------------
    # Get Source Objects
    # --------------------------------------------------

    plateau = bpy.data.objects.get("plateau")
    bing = bpy.data.objects.get("bing")

    if plateau is None:
        raise Exception("PLATEAU object not found.")

    if bing is None:
        raise Exception("BING object not found.")

    # --------------------------------------------------
    # Generate Grid
    # --------------------------------------------------

    manager = GridManager()

    manager.generate(
        min_x=CITY_MIN_X,
        min_y=CITY_MIN_Y,
        max_x=CITY_MAX_X,
        max_y=CITY_MAX_Y,
        chunk_size=CHUNK_SIZE,
        draw_labels=True,
        label_size=LABEL_SIZE,
        label_height=LABEL_HEIGHT,
    )

    manager.print_summary()

    # --------------------------------------------------
    # Create Pipeline
    # --------------------------------------------------

    pipeline = Pipeline(

        plateau_object=plateau,

        bing_object=bing,

        output_folder=OUTPUT_FOLDER,

    )

    # --------------------------------------------------
    # Test Only First Grid
    # --------------------------------------------------

    print("\n==============================")
    print("Testing First Grid")
    print("==============================")

    pipeline.process(
        manager.cells[0]
    )

    # --------------------------------------------------
    # Uncomment Later For Batch
    # --------------------------------------------------

    # pipeline.run(manager.cells)


if __name__ == "__main__":
    main()