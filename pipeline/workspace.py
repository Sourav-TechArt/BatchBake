import bpy


class Workspace:
    """
    Creates a temporary workspace.

    The original objects are never modified.

    Returns
    -------
    plateau_copy
    bing_copy
    """

    COLLECTION_NAME = "GeoBake_Workspace"

    def __init__(self):

        self.collection = None

    # --------------------------------------------------------
    # Create Workspace
    # --------------------------------------------------------

    def create(
        self,
        plateau,
        bing,
        cell,
    ):

        print(f"\nCreating Workspace : {cell.label}")

        self.clear()

        self.create_collection()

        plateau_copy = self.duplicate_object(
            source_object=plateau,
            new_name=f"Plateau_{cell.label}",
        )

        bing_copy = self.duplicate_object(
            source_object=bing,
            new_name=f"Bing_{cell.label}",
        )

        # --------------------------------------------------
        # Update Blender View Layer
        # --------------------------------------------------

        bpy.context.view_layer.update()

        # --------------------------------------------------
        # Make Plateau Copy Active
        # --------------------------------------------------

        bpy.ops.object.select_all(action='DESELECT')

        plateau_copy.select_set(True)

        bpy.context.view_layer.objects.active = plateau_copy

        print("Workspace Ready")

        return plateau_copy, bing_copy

    # --------------------------------------------------------
    # Create Collection
    # --------------------------------------------------------

    def create_collection(self):

        # Remove old collection if it somehow still exists
        old = bpy.data.collections.get(self.COLLECTION_NAME)

        if old is not None:

            for obj in list(old.objects):
                bpy.data.objects.remove(
                    obj,
                    do_unlink=True,
                )

            bpy.data.collections.remove(old)

        collection = bpy.data.collections.new(
            self.COLLECTION_NAME
        )

        bpy.context.scene.collection.children.link(
            collection
        )

        self.collection = collection

    # --------------------------------------------------------
    # Duplicate Object
    # --------------------------------------------------------

    def duplicate_object(
        self,
        source_object,
        new_name,
    ):

        if source_object is None:
            raise Exception(
                "Source object is None."
            )

        obj = source_object.copy()

        obj.data = source_object.data.copy()

        obj.animation_data_clear()

        obj.name = new_name

        self.collection.objects.link(obj)

        return obj

    # --------------------------------------------------------
    # Clear Workspace
    # --------------------------------------------------------

    def clear(self):

        collection = bpy.data.collections.get(
            self.COLLECTION_NAME
        )

        if collection is None:
            return

        for obj in list(collection.objects):

            bpy.data.objects.remove(
                obj,
                do_unlink=True,
            )

        bpy.data.collections.remove(collection)

        self.collection = None

        bpy.context.view_layer.update()