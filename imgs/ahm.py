# -----------------------------------------------
# Project: Achievability Heat Map
# # Name: ahm
# # Version 1.0.0
# # Purpose: ArcGIS Toolbox (.pyt)
# # Author: James M Roden
# # Created: Sept 2020
# # ArcGIS Version: 10.5
# # Python Version 2.7
# # PEP8
# -----------------------------------------------

from attribute_builder import AttributeBuilder
from generate_grid_id import GenerateID


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = 'Achievablity Heat Map'
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [AttributeBuilder, GenerateID]
