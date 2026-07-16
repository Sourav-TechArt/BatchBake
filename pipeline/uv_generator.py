import bpy


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
            print("No Plateau object supplied.")
            return

        print(f"\nGenerating UV : {plateau.name}")

        # --------------------------------------------------
        # Select Object
        # --------------------------------------------------

        bpy.ops.object.select_all(action='DESELECT')

        plateau.select_set(True)

        bpy.context.view_layer.objects.active = plateau

        # Make sure we're in Object Mode first
        if bpy.context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        # --------------------------------------------------
        # Enter Edit Mode
        # --------------------------------------------------

        bpy.ops.object.mode_set(mode='EDIT')

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

        bpy.ops.object.mode_set(mode='OBJECT')

        print(f"{plateau.name} UV Finished")