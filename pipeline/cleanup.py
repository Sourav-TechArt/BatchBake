import bpy


class Cleanup:
    """
    Removes the temporary GeoBake workspace after
    the current chunk has finished processing.
    """

    COLLECTION_NAME = "GeoBake_Workspace"

    def delete(self):

        collection = bpy.data.collections.get(
            self.COLLECTION_NAME
        )

        if collection is None:
            print("No workspace to clean.")
            return

        for obj in list(collection.objects):

            bpy.data.objects.remove(
                obj,
                do_unlink=True,
            )

        bpy.data.collections.remove(collection)

        print("Workspace Deleted")