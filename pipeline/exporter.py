import bpy
import os

from utils.blender_context import BlenderContext


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
            raise ValueError("Plateau object is None.")

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
        # Activate Object
        # ------------------------------------------

        BlenderContext.activate(plateau)

        bpy.context.view_layer.update()

        # ------------------------------------------
        # Optional Triangulate Modifier
        # ------------------------------------------

        tri_modifier = None

        try:

            if triangulate:

                tri_modifier = plateau.modifiers.new(
                    name="GeoBakeTriangulate",
                    type='TRIANGULATE',
                )

                tri_modifier.keep_custom_normals = True

            bpy.context.view_layer.update()

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

            print(f"Exported : {filepath}")

        except RuntimeError as e:

            raise RuntimeError(
                f"Failed to export FBX:\n{e}"
            )

        finally:

            if tri_modifier is not None:

                if tri_modifier.name in plateau.modifiers:

                    plateau.modifiers.remove(
                        tri_modifier
                    )

            BlenderContext.object_mode()

            bpy.context.view_layer.update()