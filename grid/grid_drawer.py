import bpy
import bmesh


class GridDrawer:
    """
    Draws the GeoBake grid as one mesh.

    Returns
    -------
    grid_object
        Blender mesh object.

    face_lookup
        Dictionary mapping

            polygon.index -> GridCell
    """

    GRID_NAME = "GeoBake_Grid"

    @classmethod
    def clear(cls):

        obj = bpy.data.objects.get(cls.GRID_NAME)

        if obj is None:
            return

        mesh = obj.data

        bpy.data.objects.remove(obj, do_unlink=True)

        if mesh.users == 0:
            bpy.data.meshes.remove(mesh)

    @classmethod
    def draw(cls, cells):

        cls.clear()

        mesh = bpy.data.meshes.new(cls.GRID_NAME)

        obj = bpy.data.objects.new(cls.GRID_NAME, mesh)

        bpy.context.collection.objects.link(obj)

        bm = bmesh.new()

        vertex_cache = {}

        def get_vertex(x, y):

            key = (round(x, 6), round(y, 6))

            if key in vertex_cache:
                return vertex_cache[key]

            vert = bm.verts.new((x, y, 0))

            vertex_cache[key] = vert

            return vert

        #
        # Create one quad per GridCell
        #

        for cell in cells:

            v1 = get_vertex(cell.min_x, cell.min_y)
            v2 = get_vertex(cell.max_x, cell.min_y)
            v3 = get_vertex(cell.max_x, cell.max_y)
            v4 = get_vertex(cell.min_x, cell.max_y)

            try:
                bm.faces.new((v1, v2, v3, v4))

            except ValueError:
                pass

        bm.faces.ensure_lookup_table()

        bm.to_mesh(mesh)

        bm.free()

        mesh.update()

        #
        # Display Settings
        #

        obj.show_wire = True
        obj.show_all_edges = True

        #
        # Permanent Face Lookup
        #

        face_lookup = {}

        for polygon, cell in zip(mesh.polygons, cells):

            face_lookup[polygon.index] = cell

        print("--------------------------------")
        print("GeoBake Grid")
        print("--------------------------------")
        print(f"Faces : {len(mesh.polygons)}")
        print(f"Cells : {len(cells)}")
        print("--------------------------------")

        return obj, face_lookup