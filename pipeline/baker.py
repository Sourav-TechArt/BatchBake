import bpy
import os

from utils.blender_context import BlenderContext
from .material_setup import MaterialSetup


class Baker:
    """
    GeoBake Baker

    Bakes Bing -> Plateau using Selected to Active.
    """

    def __init__(self):

        self.material = MaterialSetup()

    # --------------------------------------------------
    # Bake
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

        if plateau is None:
            raise ValueError("Plateau object is None.")

        if bing is None:
            raise ValueError("Bing object is None.")

        print(f"\nBaking : {cell.label}")

        self.setup_cycles(samples)

        for bake in bake_distances:

            if not bake["enabled"]:
                continue

            distance = bake["distance"]

            print(f"\nBake Distance : {distance}m")

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

            bpy.context.view_layer.update()

            try:

                bpy.ops.object.bake(
                    type='DIFFUSE'
                )

                self.save_image(

                    image,

                    output_folder,

                    cell,

                    distance,

                )

            except RuntimeError as e:

                print(f"Bake failed ({distance}m)")

                print(e)

        BlenderContext.object_mode()

        print("\nBake Finished")

    # --------------------------------------------------
    # Setup Cycles
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
    # Bake Settings
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
    # Select Objects
    # --------------------------------------------------

    def select_objects(
        self,
        plateau,
        bing,
    ):

        BlenderContext.activate_multiple(

            active_object=plateau,

            selected_objects=[bing, plateau],

        )

    # --------------------------------------------------
    # Save Image
    # --------------------------------------------------

    def save_image(
        self,
        image,
        output_folder,
        cell,
        cage_distance,
    ):

        if image is None:
            raise ValueError("Bake image is None.")

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