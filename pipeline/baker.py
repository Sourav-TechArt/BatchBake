import bpy
import os

from .material_setup import MaterialSetup


class Baker:
    """
    GeoBake Baker

    Bakes Bing -> Plateau using Selected to Active.
    """

    def __init__(self):

        self.material = MaterialSetup()

    # --------------------------------------------------

    def bake(
        self,
        plateau,
        bing,
        cell,
        output_folder,
        image_size,
        samples,
        margin,
        bake_distances,
    ):

        print(f"\nBaking : {cell.label}")

        self.setup_cycles(samples)

        for bake in bake_distances:

            if not bake["enabled"]:
                continue

            distance = bake["distance"]

            print(f"\nBake {distance}m")

            image = self.material.prepare(

                plateau=plateau,

                cell=cell,

                cage_distance=distance,

                image_size=image_size,

            )

            self.setup_bake_settings(

                cage_distance=distance,

                margin=margin,

            )

            self.select_objects(

                plateau,

                bing,

            )

            bpy.ops.object.bake(
                type='DIFFUSE'
            )

            self.save_image(

                image,

                output_folder,

                cell,

                distance,

            )

        print("\nBake Finished")

    # --------------------------------------------------

    def setup_cycles(
        self,
        samples,
    ):

        scene = bpy.context.scene

        scene.render.engine = 'CYCLES'

        scene.cycles.device = 'GPU'

        scene.cycles.samples = samples

    # --------------------------------------------------

    def setup_bake_settings(
        self,
        cage_distance,
        margin,
    ):

        scene = bpy.context.scene

        scene.render.bake.use_selected_to_active = True

        scene.render.bake.use_clear = True

        scene.render.bake.margin_type = 'ADJACENT_FACES'

        scene.render.bake.margin = margin

        scene.render.bake.max_ray_distance = cage_distance

        scene.render.bake.cage_extrusion = cage_distance

        scene.render.bake.use_pass_direct = False

        scene.render.bake.use_pass_indirect = False

        scene.render.bake.use_pass_color = True

    # --------------------------------------------------

    def select_objects(
        self,
        plateau,
        bing,
    ):

        bpy.ops.object.select_all(action='DESELECT')

        bing.select_set(True)

        plateau.select_set(True)

        bpy.context.view_layer.objects.active = plateau

    # --------------------------------------------------

    def save_image(
        self,
        image,
        output_folder,
        cell,
        cage_distance,
    ):

        folder = os.path.join(
            output_folder,
            cell.label,
        )

        os.makedirs(
            folder,
            exist_ok=True,
        )

        filepath = os.path.join(

            folder,

            f"{cell.label}_Bake_{cage_distance:02d}m.png",

        )

        image.filepath_raw = filepath

        image.file_format = 'PNG'

        image.save()

        print(f"Saved : {filepath}")