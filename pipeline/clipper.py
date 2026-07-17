import os

print("=" * 60)
print("LOADED CLIPPER:")
print(__file__)
print("=" * 60)
import bpy

from utils.blender_context import BlenderContext


class Clipper:
    """
    Clips duplicated Plateau and Bing meshes
    to the current GridCell.
    """

    CLIP_MARGIN = 1.0
    CLIP_HEIGHT = 5000.0

    # ---------------------------------------------------------
    # Clip Both Meshes
    # ---------------------------------------------------------

    def clip(
        self,
        plateau,
        bing,
        cell,
    ):

        print(f"\nClipping Chunk : {cell.label}")

        cube = self.create_clip_box(cell)

        try:

            self.boolean_object(
                plateau,
                cube,
            )

            self.boolean_object(
                bing,
                cube,
            )

        finally:

            if cube is not None and cube.name in bpy.data.objects:

                bpy.data.objects.remove(
                    cube,
                    do_unlink=True,
                )

            BlenderContext.ensure_view_layer()

        print("Clipping Finished")

    # ---------------------------------------------------------
    # Create Clip Box
    # ---------------------------------------------------------

    def create_clip_box(self, cell):

        width = cell.max_x - cell.min_x
        height = cell.max_y - cell.min_y

        center_x = (cell.min_x + cell.max_x) * 0.5
        center_y = (cell.min_y + cell.max_y) * 0.5

        # Safe even if there is no active object
        BlenderContext.object_mode()

        BlenderContext.deselect_all()

        bpy.ops.mesh.primitive_cube_add(
            location=(center_x, center_y, 0)
        )

        cube = bpy.context.active_object

        cube.name = "GeoBake_ClipBox"

        cube.scale = (
            (width + self.CLIP_MARGIN) * 0.5,
            (height + self.CLIP_MARGIN) * 0.5,
            self.CLIP_HEIGHT,
        )

        BlenderContext.ensure_view_layer()

        return cube

    # ---------------------------------------------------------
    # Boolean One Object
    # ---------------------------------------------------------

    def boolean_object(
        self,
        obj,
        cutter,
    ):

        if obj is None:
            raise ValueError("Object is None.")

        if cutter is None:
            raise ValueError("Clip box is None.")

        if obj.name not in bpy.data.objects:
            raise ValueError(f"Object '{obj.name}' no longer exists.")

        BlenderContext.activate(obj)

        old_modifier = obj.modifiers.get("GeoBakeBoolean")

        if old_modifier:
            obj.modifiers.remove(old_modifier)

        modifier = obj.modifiers.new(
            name="GeoBakeBoolean",
            type='BOOLEAN',
        )

        modifier.operation = 'INTERSECT'
        modifier.object = cutter

        BlenderContext.ensure_view_layer()

        try:

            bpy.ops.object.modifier_apply(
                modifier=modifier.name,
            )

            print(f"{obj.name} clipped")

        except RuntimeError as e:

            raise RuntimeError(
                f"Boolean failed on '{obj.name}':\n{e}"
            )

        finally:

            BlenderContext.ensure_view_layer()

