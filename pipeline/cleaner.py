import bpy
import bmesh

from utils.blender_context import BlenderContext


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
            raise ValueError("Object is None.")

        if obj.name not in bpy.data.objects:
            raise ValueError(f"Object '{obj.name}' no longer exists.")

        # ---------------------------------------
        # Activate Object
        # ---------------------------------------

        BlenderContext.activate(obj)

        # ---------------------------------------
        # Enter Edit Mode
        # ---------------------------------------

        BlenderContext.edit_mode()

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

        # ---------------------------------------
        # Update Mesh
        # ---------------------------------------

        bmesh.update_edit_mesh(
            obj.data,
            loop_triangles=True,
            destructive=True,
        )

        BlenderContext.ensure_view_layer()

        # ---------------------------------------
        # Return to Object Mode
        # ---------------------------------------

        BlenderContext.object_mode()

        print(f"{obj.name} cleaned")