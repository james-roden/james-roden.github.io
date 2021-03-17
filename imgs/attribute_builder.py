# -----------------------------------------------
# Project: Achievability Heat Map
# # Name: attribute_builder
# # Version 1.0.0
# # Purpose: ArcGIS tool to build the attributes for a tessellation grid using the JSON data provided
# # Author: James M Roden
# # Created: Sept 2020
# # ArcGIS Version: 10.5
# # Python Version 2.7
# # PEP8
# -----------------------------------------------

import arcpy
from heat_map import HeatMap


class AttributeBuilder(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Attribute Builder"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        parameter_0 = arcpy.Parameter(
            displayName='Input Grid',
            name='input_grid',
            datatype='GPFeatureLayer',
            parameterType='Required',
            direction='Input')

        parameter_1 = arcpy.Parameter(
            displayName='JSON Data File',
            name='json_data',
            datatype='DEFile',
            parameterType='Required',
            direction='Input')

        parameter_1.filter.list = ['json']

        parameters = [parameter_0, parameter_1]
        return parameters

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        arcpy.env.workspace = r'in_memory'
        arcpy.env.scratchWorkspace = r'in_memory'
        arcpy.CheckOutExtension("Spatial")
        arcpy.env.overwriteOutput = True
        arcpy.env.qualifiedFieldNames = False
        tessellation_file = parameters[0].valueAsText
        json_file = parameters[1].valueAsText

        hm = HeatMap(tessellation_file, json_file)
        hm.populate_grid()

        return
