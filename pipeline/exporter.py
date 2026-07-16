import bpy
import os


class Exporter:
    """
    Exports the processed Plateau chunk as an FBX.

    Unreal Friendly
        - Triangulate
        - Selected Object Only
        - Mesh Modifiers Applied
    """

    # --------------------------------------------------
    # Export
    # --------------------------------------------------

    def export(
        self,
        plateau,
        cell,
        output_folder,
        triangulate=True,
    ):

        if plateau is None:
            return

        # ------------------------------------------
        # Create Output Folder
        # ------------------------------------------

        chunk_folder = os.path.join(
            output_folder,
            cell.label,
        )

        os.makedirs(
            chunk_folder,
            exist_ok=True,
        )

        filepath = os.path.join(
            chunk_folder,
            f"{cell.label}.fbx",
        )

        # ------------------------------------------
        # Select Object
        # ------------------------------------------

        bpy.ops.object.select_all(action='DESELECT')

        plateau.select_set(True)

        bpy.context.view_layer.objects.active = plateau

        if bpy.context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        # ------------------------------------------
        # Optional Triangulate Modifier
        # ------------------------------------------

        tri_modifier = None

        if triangulate:

            tri_modifier = plateau.modifiers.new(
                name="GeoBakeTriangulate",
                type='TRIANGULATE',
            )

            tri_modifier.keep_custom_normals = True

        # ------------------------------------------
        # Export FBX
        # ------------------------------------------

        bpy.ops.export_scene.fbx(

            filepath=filepath,

            use_selection=True,

            object_types={'MESH'},

            use_mesh_modifiers=True,

            mesh_smooth_type='FACE',

            bake_space_transform=False,

            axis_forward='-Z',

            axis_up='Y',

            apply_scale_options='FBX_SCALE_ALL',

            add_leaf_bones=False,

            use_armature_deform_only=False,

            bake_anim=False,

            path_mode='AUTO',

            embed_textures=False,

        )

        # ------------------------------------------
        # Remove Temporary Modifier
        # ------------------------------------------

        if tri_modifier:

            plateau.modifiers.remove(
                tri_modifier
            )

        print(f"Exported : {filepath}")