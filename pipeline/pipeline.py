from .workspace import Workspace
from .clipper import Clipper

from .uv_generator import UVGenerator
from .workspace_saver import WorkspaceSaver
from .baker import Baker
from .exporter import Exporter
from .cleanup import Cleanup

try:
    from .cleaner import Cleaner
except Exception:
    import traceback
    traceback.print_exc()
    raise


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
        # ---------------------------------------

        self.image_size = 1024

        self.samples = 10

        self.margin = 2

        self.triangulate = True

        self.bake_distances = [

            {"enabled": True, "distance": 2},
            {"enabled": True, "distance": 4},
            {"enabled": True, "distance": 6},
            {"enabled": False, "distance": 8},
            {"enabled": False, "distance": 10},
            {"enabled": False, "distance": 12},
            {"enabled": False, "distance": 16},
            {"enabled": False, "distance": 20},

        ]

    # -------------------------------------------------------
    # Mesh Validation
    # -------------------------------------------------------

    def has_mesh(self, obj):
        """
        Returns True if object contains usable mesh geometry.
        """

        if obj is None:
            return False

        if obj.type != "MESH":
            return False

        if len(obj.data.polygons) == 0:
            return False

        return True

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
        # Skip Empty Chunks
        # ---------------------------------------

        if not self.has_mesh(plateau_copy):

            print(f"\nSkipping {cell.label}")
            print("Reason : Empty Plateau mesh")

            self.cleanup.delete()

            return

        if not self.has_mesh(bing_copy):

            print(f"\nSkipping {cell.label}")
            print("Reason : Empty Bing mesh")

            self.cleanup.delete()

            return

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

            try:

                self.process(cell)

            except Exception as e:

                print(f"\n✗ {cell.label} Failed")
                print(e)

                try:
                    self.cleanup.delete()
                except Exception:
                    pass

                continue

        print("\n========================================")
        print("GeoBake Batch Finished")
        print("========================================")