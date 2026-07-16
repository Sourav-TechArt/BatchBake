from .grid_generator import GridGenerator
from .grid_drawer import GridDrawer
from .grid_labeler import GridLabeler


class GridManager:
    """
    Central manager for the GeoBake Grid System.
    """

    def __init__(self):

        # All GridCell objects
        self.cells = []

        # Label -> GridCell
        self.label_lookup = {}

        # Polygon Index -> GridCell
        self.face_lookup = {}

        # Blender Grid Object
        self.grid_object = None

        # Current Selection
        self.selected_face = None
        self.selected_cell = None

    # ----------------------------------------------------------
    # Generate Grid
    # ----------------------------------------------------------

    def generate(
        self,
        min_x,
        min_y,
        max_x,
        max_y,
        chunk_size,
        draw_labels=True,
        label_size=40,
        label_height=2,
    ):

        generator = GridGenerator(
            min_x=min_x,
            min_y=min_y,
            max_x=max_x,
            max_y=max_y,
            chunk_size=chunk_size,
        )

        self.cells = generator.generate()

        # ------------------------------------------
        # Build Label Lookup
        # ------------------------------------------

        self.label_lookup.clear()

        for cell in self.cells:
            self.label_lookup[cell.label] = cell

        # ------------------------------------------
        # Draw Grid
        # ------------------------------------------

        self.grid_object, self.face_lookup = GridDrawer.draw(
            self.cells
        )

        # ------------------------------------------
        # Labels
        # ------------------------------------------

        if draw_labels:

            GridLabeler.create_labels(
                self.cells,
                text_size=label_size,
                height=label_height,
            )

        return self.grid_object

    # ----------------------------------------------------------
    # Get Cell By Face
    # ----------------------------------------------------------

    def get_cell(self, face_index):

        return self.face_lookup.get(face_index)

    # ----------------------------------------------------------
    # Get Cell By Label
    # ----------------------------------------------------------

    def get_cell_by_label(self, label):

        return self.label_lookup.get(label)

    # ----------------------------------------------------------
    # Select Face
    # ----------------------------------------------------------

    def select_face(self, face_index):

        self.selected_face = face_index

        self.selected_cell = self.get_cell(face_index)

        return self.selected_cell

    # ----------------------------------------------------------
    # Print Summary
    # ----------------------------------------------------------

    def print_summary(self):

        print("\n--------------------------------------")
        print("GeoBake Grid Summary")
        print("--------------------------------------")
        print(f"Grid Object : {self.grid_object.name}")
        print(f"Cells       : {len(self.cells)}")
        print(f"Faces       : {len(self.face_lookup)}")
        print("--------------------------------------")

    # ----------------------------------------------------------
    # Print Face Lookup
    # ----------------------------------------------------------

    def print_lookup(self):

        print("\nFace Lookup\n")

        for face_index, cell in self.face_lookup.items():

            print(
                f"Face {face_index:03d} -> {cell.label}"
            )

    # ----------------------------------------------------------
    # Print Cell Information
    # ----------------------------------------------------------

    def print_cells(self):

        print("\nGrid Cells\n")

        for cell in self.cells:

            print(
                f"{cell.label:>3} | "
                f"X: {cell.min_x:8.1f} -> {cell.max_x:<8.1f} | "
                f"Y: {cell.min_y:8.1f} -> {cell.max_y:<8.1f}"
            )

    # ----------------------------------------------------------
    # Clear
    # ----------------------------------------------------------

    def clear(self):

        GridDrawer.clear()
        GridLabeler.clear()

        self.cells.clear()
        self.label_lookup.clear()
        self.face_lookup.clear()

        self.selected_face = None
        self.selected_cell = None

        self.grid_object = None