import bpy
import os


class WorkspaceSaver:
    """
    Saves the current Blender file before baking.

    This acts as a recovery checkpoint.
    """

    OUTPUT_FOLDER = r"E:\Work\MAP_Rnd\GeoBake\BatchBake"

    def save(self, cell):

        folder = os.path.join(
            self.OUTPUT_FOLDER,
            cell.label,
        )

        os.makedirs(folder, exist_ok=True)

        filepath = os.path.join(
            folder,
            f"{cell.label}_Workspace.blend",
        )

        bpy.ops.wm.save_as_mainfile(
            filepath=filepath,
            copy=True,
        )

        print(f"Workspace Saved : {filepath}")