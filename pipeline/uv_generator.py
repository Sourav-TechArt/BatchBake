import bpy

from utils.blender_context import BlenderContext


class UVGenerator:
    """
    Generates UVs for the processed Plateau mesh.

    Workflow
        - Smart UV Project
        - Pack Islands
    """

    SMART_UV_ANGLE = 1.151917  # Its a Radian Value not degree as Blender use radian value not degree 
    ISLAND_MARGIN = 0.0
    PACK_MARGIN = 0.0

    # --------------------------------------------------
    # Generate UV
    # --------------------------------------------------

    def generate(
        self,
        plateau,
    ):

        if plateau is None:
            raise ValueError("Plateau object is None.")

        if plateau.name not in bpy.data.objects:
            raise ValueError(
                f"Object '{plateau.name}' no longer exists."
            )

        print(f"\nGenerating UV : {plateau.name}")

        # --------------------------------------------------
        # Activate Object
        # --------------------------------------------------

        BlenderContext.activate(plateau)

        # --------------------------------------------------
        # Enter Edit Mode
        # --------------------------------------------------

        BlenderContext.edit_mode()

        bpy.ops.mesh.select_all(action='SELECT')

        # --------------------------------------------------
        # Smart UV Project
        # --------------------------------------------------

        bpy.ops.uv.smart_project(
            angle_limit=self.SMART_UV_ANGLE,
            margin_method='SCALED',
            island_margin=self.ISLAND_MARGIN,
            area_weight=0.0,
            correct_aspect=True,
            scale_to_bounds=True,
)

        # --------------------------------------------------
        # Pack Islands
        # --------------------------------------------------

        bpy.ops.uv.select_all(action='SELECT')

        bpy.ops.uv.pack_islands(
            shape_method='CONCAVE',
            rotate=True,
            rotate_method='ANY',
            scale=True,
            margin_method='SCALED',
            margin=self.PACK_MARGIN,
            merge_overlap=False,
            udim_source='CLOSEST_UDIM',
        )

        BlenderContext.ensure_view_layer()

        # --------------------------------------------------
        # Return To Object Mode
        # --------------------------------------------------

        BlenderContext.object_mode()

        print(f"{plateau.name} UV Finished")