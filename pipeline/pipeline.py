from .workspace import Workspace
from .clipper import Clipper
from .cleaner import Cleaner
from .uv_generator import UVGenerator
from .workspace_saver import WorkspaceSaver
from .baker import Baker
from .exporter import Exporter
from .cleanup import Cleanup


class Pipeline:
    """
    GeoBake Processing Pipeline

    Pipeline

        Workspace
            ↓
        Clip
            ↓
        Clean
            ↓
        Generate UV
            ↓
        Save Workspace
            ↓
        Bake
            ↓
        Export FBX
            ↓
        Cleanup
    """

    def __init__(
        self,
        plateau_object,
        bing_object,
        output_folder,
    ):

        # Original scene objects
        self.plateau = plateau_object
        self.bing = bing_object

        # Output
        self.output_folder = output_folder

        # Pipeline Modules
        self.workspace = Workspace()
        self.clipper = Clipper()
        self.cleaner = Cleaner()
        self.uv = UVGenerator()
        self.workspace_saver = WorkspaceSaver()
        self.baker = Baker()
        self.exporter = Exporter()
        self.cleanup = Cleanup()

        # ---------------------------------------
        # Temporary Settings
        # (Later these will come from UI)
        # ---------------------------------------

        self.image_size = 8192

        self.samples = 10

        self.margin = 2

        self.triangulate = True

        self.bake_distances = [

            {"enabled": True, "distance": 2},
            {"enabled": True, "distance": 4},
            {"enabled": True, "distance": 6},
            {"enabled": True, "distance": 8},
            {"enabled": True, "distance": 10},
            {"enabled": True, "distance": 12},
            {"enabled": True, "distance": 16},
            {"enabled": False, "distance": 20},

        ]

    # -------------------------------------------------------
    # Process One Grid Cell
    # -------------------------------------------------------

    def process(self, cell):

        print("\n========================================")
        print(f"Processing Chunk : {cell.label}")
        print("========================================")

        # ---------------------------------------
        # Create Workspace
        # ---------------------------------------

        plateau_copy, bing_copy = self.workspace.create(

            self.plateau,

            self.bing,

            cell,

        )

        # ---------------------------------------
        # Clip
        # ---------------------------------------

        self.clipper.clip(

            plateau_copy,

            bing_copy,

            cell,

        )

        # ---------------------------------------
        # Clean
        # ---------------------------------------

        self.cleaner.clean(

            plateau_copy,

            bing_copy,

        )

        # ---------------------------------------
        # Generate UV
        # ---------------------------------------

        self.uv.generate(

            plateau_copy,

        )

        # ---------------------------------------
        # Save Workspace
        # ---------------------------------------

        self.workspace_saver.save(

            cell,

        )

        # ---------------------------------------
        # Bake
        # ---------------------------------------

        self.baker.bake(

            plateau_copy,

            bing_copy,

            cell,

            self.output_folder,

            self.image_size,

            self.samples,

            self.margin,

            self.bake_distances,

        )

        # ---------------------------------------
        # Export FBX
        # ---------------------------------------

        self.exporter.export(

            plateau_copy,

            cell,

            self.output_folder,

            self.triangulate,

        )

        # ---------------------------------------
        # Cleanup
        # ---------------------------------------

        self.cleanup.delete()

        print(f"\n✓ {cell.label} Finished")

    # -------------------------------------------------------
    # Batch Process
    # -------------------------------------------------------

    def run(self, cells):

        print("\n========================================")
        print("GeoBake Batch Started")
        print("========================================")

        total = len(cells)

        for index, cell in enumerate(cells):

            print("\n----------------------------------------")
            print(f"Chunk {index + 1} / {total}")
            print("----------------------------------------")

            self.process(cell)

        print("\n========================================")
        print("GeoBake Batch Finished")
        print("========================================")