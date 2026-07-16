import bpy


class MaterialSetup:
    """
    Creates a bake material and bake image
    for the processed Plateau mesh.
    """

    MATERIAL_NAME = "GeoBake_Material"

    # ---------------------------------------------------
    # Prepare Material
    # ---------------------------------------------------

    def prepare(
        self,
        plateau,
        cell,
        cage_distance,
        image_size,
    ):

        if plateau is None:
            return None

        print(f"\nPreparing Material : {plateau.name}")

        self.remove_materials(plateau)

        material = self.create_material()

        plateau.data.materials.append(material)

        image = self.create_image(
            cell,
            cage_distance,
            image_size,
        )

        self.setup_nodes(
            material,
            image,
        )

        print("Material Ready")

        return image

    # ---------------------------------------------------
    # Remove Existing Materials
    # ---------------------------------------------------

    def remove_materials(
        self,
        obj,
    ):

        obj.data.materials.clear()

    # ---------------------------------------------------
    # Create Material
    # ---------------------------------------------------

    def create_material(self):

        material = bpy.data.materials.new(
            self.MATERIAL_NAME
        )

        material.use_nodes = True

        return material

    # ---------------------------------------------------
    # Create Bake Image
    # ---------------------------------------------------

    def create_image(
        self,
        cell,
        cage_distance,
        image_size,
    ):

        image_name = (
            f"{cell.label}_Bake_{cage_distance:02d}m"
        )

        image = bpy.data.images.new(

            name=image_name,

            width=image_size,

            height=image_size,

            alpha=True,

            float_buffer=False,

        )

        image.generated_type = 'BLANK'

        image.generated_color = (

            0.0,
            0.0,
            0.0,
            0.0,

        )

        image.file_format = 'PNG'

        return image

    # ---------------------------------------------------
    # Build Material Nodes
    # ---------------------------------------------------

    def setup_nodes(
        self,
        material,
        image,
    ):

        nodes = material.node_tree.nodes
        links = material.node_tree.links

        nodes.clear()

        output = nodes.new(
            "ShaderNodeOutputMaterial"
        )

        output.location = (400, 0)

        bsdf = nodes.new(
            "ShaderNodeBsdfPrincipled"
        )

        bsdf.location = (150, 0)

        tex = nodes.new(
            "ShaderNodeTexImage"
        )

        tex.location = (-250, 0)

        tex.image = image

        links.new(
            bsdf.outputs["BSDF"],
            output.inputs["Surface"],
        )

        # Active bake target
        nodes.active = tex