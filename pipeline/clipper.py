import bpy


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

        self.boolean_object(
            plateau,
            cube,
        )

        self.boolean_object(
            bing,
            cube,
        )

        bpy.data.objects.remove(
            cube,
            do_unlink=True,
        )

        print("Clipping Finished")

    # ---------------------------------------------------------
    # Create Clip Box
    # ---------------------------------------------------------

    def create_clip_box(self, cell):

        width = cell.max_x - cell.min_x
        height = cell.max_y - cell.min_y

        center_x = (cell.min_x + cell.max_x) * 0.5
        center_y = (cell.min_y + cell.max_y) * 0.5

        bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.mesh.primitive_cube_add()

        cube = bpy.context.active_object

        cube.name = "GeoBake_ClipBox"

        cube.location = (
            center_x,
            center_y,
            0,
        )

        cube.scale = (
            (width + self.CLIP_MARGIN) * 0.5,
            (height + self.CLIP_MARGIN) * 0.5,
            self.CLIP_HEIGHT,
        )

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
            return

        bpy.ops.object.select_all(action='DESELECT')

        obj.select_set(True)

        bpy.context.view_layer.objects.active = obj

        modifier = obj.modifiers.new(
            name="GeoBakeBoolean",
            type='BOOLEAN',
        )

        modifier.operation = 'INTERSECT'

        modifier.object = cutter

        bpy.ops.object.modifier_apply(
            modifier=modifier.name,
        )

        print(f"{obj.name} clipped")