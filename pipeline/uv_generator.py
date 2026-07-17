import bpy

from utils.blender_context import BlenderContext


class UVGenerator:
    """
    Generates UVs for the processed Plateau mesh.

    V1
        - Smart UV Project
        - Pack Islands
    """

    SMART_UV_ANGLE = 66.0
    ISLAND_MARGIN = 0.001
    PACK_MARGIN = 0.001
    ROTATE_ISLANDS = True

    # --------------------------------------------------
    # Generate UV
    # --------------------------------------------------

    def generate(self, plateau):

        if plateau is None:
            raise ValueError("Plateau object is None.")

        print(f"\nGenerating UV : {plateau.name}")

        # --------------------------------------------------
        # Activate Object
        # --------------------------------------------------

        BlenderContext.activate(plateau)

        # --------------------------------------------------
        # Enter Edit Mode
        # --------------------------------------------------

        bpy.ops.object.mode_set(mode='EDIT')

        # --------------------------------------------------
        # Select All Faces
        # --------------------------------------------------

        bpy.ops.mesh.select_all(action='SELECT')

        # --------------------------------------------------
        # Smart UV Project
        # --------------------------------------------------

        bpy.ops.uv.smart_project(
            angle_limit=self.SMART_UV_ANGLE,
            island_margin=self.ISLAND_MARGIN,
            area_weight=0.0,
            correct_aspect=True,
            scale_to_bounds=False,
        )

        # --------------------------------------------------
        # Pack Islands
        # --------------------------------------------------

        bpy.ops.uv.select_all(action='SELECT')

        bpy.ops.uv.pack_islands(
            rotate=self.ROTATE_ISLANDS,
            margin=self.PACK_MARGIN,
        )

        # --------------------------------------------------
        # Return To Object Mode
        # --------------------------------------------------

        BlenderContext.object_mode()

        bpy.context.view_layer.update()

        print(f"{plateau.name} UV Finished")