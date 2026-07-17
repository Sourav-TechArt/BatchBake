import bpy


class BlenderContext:
    """
    Utility class for safely managing Blender context.

    Every pipeline module should use this instead of directly
    calling bpy.ops.object.mode_set(), select_all(), etc.
    """

    # --------------------------------------------------
    # View Layer
    # --------------------------------------------------

    @staticmethod
    def ensure_view_layer():
        bpy.context.view_layer.update()

    # --------------------------------------------------
    # Object Mode
    # --------------------------------------------------

    @staticmethod
    def object_mode():
        """
        Safely switch to Object Mode.
        """

        active = bpy.context.view_layer.objects.active

        # No active object
        if active is None:
            return

        # Already in Object Mode
        if active.mode == 'OBJECT':
            return

        try:
            bpy.ops.object.mode_set(mode='OBJECT')
        except RuntimeError:
            return

        BlenderContext.ensure_view_layer()

    # --------------------------------------------------
    # Edit Mode
    # --------------------------------------------------

    @staticmethod
    def edit_mode():
        """
        Safely switch to Edit Mode.
        """

        active = bpy.context.view_layer.objects.active

        if active is None:
            raise RuntimeError("No active object to enter Edit Mode.")

        if active.mode == 'EDIT':
            return

        BlenderContext.object_mode()

        try:
            bpy.ops.object.mode_set(mode='EDIT')
        except RuntimeError:
            return

        BlenderContext.ensure_view_layer()

    # --------------------------------------------------
    # Deselect All
    # --------------------------------------------------

    @staticmethod
    def deselect_all():
        """
        Deselect every selected object.
        Uses Blender Data API instead of bpy.ops.
        """

        for obj in bpy.context.selected_objects:
            obj.select_set(False)

        bpy.context.view_layer.objects.active = None

        BlenderContext.ensure_view_layer()

    # --------------------------------------------------
    # Activate Single Object
    # --------------------------------------------------

    @staticmethod
    def activate(obj):
        """
        Make one object active and selected.
        """

        if obj is None:
            raise ValueError("Cannot activate None object.")

        if obj.name not in bpy.data.objects:
            raise ValueError(f"Object '{obj.name}' no longer exists.")

        BlenderContext.object_mode()

        BlenderContext.deselect_all()

        obj.select_set(True)

        bpy.context.view_layer.objects.active = obj

        BlenderContext.ensure_view_layer()

    # --------------------------------------------------
    # Activate Multiple Objects
    # --------------------------------------------------

    @staticmethod
    def activate_multiple(
        active_object,
        selected_objects,
    ):
        """
        Used for Selected-to-Active baking.
        """

        if active_object is None:
            raise ValueError("Active object is None.")

        if active_object.name not in bpy.data.objects:
            raise ValueError(
                f"Object '{active_object.name}' no longer exists."
            )

        BlenderContext.object_mode()

        BlenderContext.deselect_all()

        for obj in selected_objects:

            if obj is None:
                continue

            if obj.name not in bpy.data.objects:
                continue

            obj.select_set(True)

        bpy.context.view_layer.objects.active = active_object

        BlenderContext.ensure_view_layer()