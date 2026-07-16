import bpy
from math import radians


class GridLabeler:

    COLLECTION_NAME = "GeoBake_Labels"

    @classmethod
    def clear(cls):
        """
        Remove all existing labels.
        """

        collection = bpy.data.collections.get(cls.COLLECTION_NAME)

        if collection is None:
            return

        # Delete objects
        for obj in list(collection.objects):
            bpy.data.objects.remove(obj, do_unlink=True)

        # Delete collection
        bpy.data.collections.remove(collection)

    @classmethod
    def create_labels(
        cls,
        cells,
        text_size=80,
        height=0.5,
    ):
        """
        Creates one text object per grid cell.
        """

        cls.clear()

        collection = bpy.data.collections.new(cls.COLLECTION_NAME)
        bpy.context.scene.collection.children.link(collection)

        for cell in cells:

            curve = bpy.data.curves.new(
                name=cell.label,
                type='FONT'
            )

            curve.body = cell.label
            curve.size = text_size
            curve.align_x = 'CENTER'
            curve.align_y = 'CENTER'

            text_obj = bpy.data.objects.new(
                cell.label,
                curve
            )

            cx, cy = cell.center

            text_obj.location = (
                cx,
                cy,
                height
            )

            # Rotate so text is readable from Top View
            text_obj.rotation_euler = (
                radians(0),
                0,
                0
            )

            collection.objects.link(text_obj)

        return collection