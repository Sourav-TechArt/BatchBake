import bpy
import bmesh


class Cleaner:
    """
    Cleans Plateau and Bing meshes after clipping.

    Current Operations:
        - Remove Duplicate Vertices
        - Recalculate Normals
    """

    MERGE_DISTANCE = 0.0001

    # -------------------------------------------------------
    # Clean Both Meshes
    # -------------------------------------------------------

    def clean(
        self,
        plateau,
        bing,
    ):

        print("\nCleaning Meshes")

        self.clean_object(plateau)

        self.clean_object(bing)

        print("Cleaning Finished")

    # -------------------------------------------------------
    # Clean One Object
    # -------------------------------------------------------

    def clean_object(
        self,
        obj,
    ):

        if obj is None:
            return

        bpy.ops.object.select_all(action='DESELECT')

        obj.select_set(True)

        bpy.context.view_layer.objects.active = obj

        if bpy.context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.object.mode_set(mode='EDIT')

        bm = bmesh.from_edit_mesh(obj.data)

        # ---------------------------------------
        # Remove Duplicate Vertices
        # ---------------------------------------

        bmesh.ops.remove_doubles(
            bm,
            verts=bm.verts,
            dist=self.MERGE_DISTANCE,
        )

        # ---------------------------------------
        # Recalculate Normals
        # ---------------------------------------

        bmesh.ops.recalc_face_normals(
            bm,
            faces=bm.faces,
        )

        bmesh.update_edit_mesh(obj.data)

        bpy.ops.object.mode_set(mode='OBJECT')

        print(f"{obj.name} cleaned")