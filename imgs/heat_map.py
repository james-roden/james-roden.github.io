# -----------------------------------------------
# Project: Achievability Heat Map
# Name: heat_map
# Version 1.0.0
# Purpose: HeatMap class to run geospatial analysis on a tessellation grid
# Author: James M Roden
# Created: Sept 2020
# ArcGIS Version: 10.5
# Python Version 2.7
# PEP8
# -----------------------------------------------
import arcpy


class HeatMap:

    def __init__(self, tessellation_grid, json_data):
        self.grid = tessellation_grid
        self.json_data = json_data
        self.fields_names = [f.name for f in arcpy.ListFields(tessellation_grid)]

    def zonal_statistics(self, data_type, data_source):
        """Performs zonal statistics on input raster and stores data in the tessellation grid.

        Creates mean, max, & min statistical fields in self.grid and populates them using the input raster, data_source
        data_type and data_source are provided by a specifically formatted JSON file.

        """

        # Local variables
        layer_name = data_type + '_grdlyr'
        table = data_type + '_znlsts'
        join_field = 'GRID_ID'

        # Create fields...
        statistics = ['MEAN', 'MAX', 'MIN']
        field_names = [data_type + '_' + i for i in statistics]
        for field in field_names:
            if not self.__field_exists(field):
                arcpy.AddField_management(self.grid, field, "FLOAT")

        # Run zonal Stats
        arcpy.sa.ZonalStatisticsAsTable(self.grid, 'GRID_ID', data_source, table, statistics_type='MIN_MAX_MEAN')

        # Create feature layer for join and calculate to work properly, as per ESRI docs...
        arcpy.MakeFeatureLayer_management(self.grid, layer_name)
        arcpy.AddJoin_management(layer_name, join_field, table, join_field)

        # Calculate Fields...
        for stat, field in zip(statistics, field_names):
            arcpy.CalculateField_management(layer_name, field, '!' + stat + '!', 'PYTHON')

        self.fields_names = [f.name for f in arcpy.ListFields(self.grid)]

    def spatial_join(self, data_type, data_source, grid_fields, data_fields, field_types, merge_rules, join_delimiters):
        """Performs a spatial join with self.grid and the input data, data_source.

        Creates a field for each element in data_fields in self.grid ~grid_fields and populates them using the field
        mapping parameters merge_types and join_delimiters. data_type, data_source, grid_fields, data_fields,
        field_types, merge_rules, & join_delimiters are provided by a specifically formatted JSON file.

        """

        # Create feature layer as per ESRI docs...
        layer_name = 'grid_layer'
        arcpy.MakeFeatureLayer_management(self.grid, layer_name)

        # Create fields
        for field, field_type in zip(grid_fields, field_types):
            if not self.__field_exists(field):
                arcpy.AddField_management(self.grid, field, field_type)

        fms = arcpy.FieldMappings()
        for field, merge_rule, join_delimiter in zip(data_fields, merge_rules, join_delimiters):
            fm = arcpy.FieldMap()
            fm.addInputField(data_source, field)
            fm.mergeRule = merge_rule
            fm.joinDelimiter = join_delimiter
            grid_id_fm = arcpy.FieldMap()
            grid_id_fm.addInputField(layer_name, 'GRID_ID')
            fms.addFieldMap(fm)
            fms.addFieldMap(grid_id_fm)

        join_table = arcpy.SpatialJoin_analysis(self.grid, data_source, None, field_mapping=fms)

        # Perform Join
        arcpy.AddJoin_management(layer_name, 'GRID_ID', join_table, 'GRID_ID')

        # Calculate fields in grid
        for i, j in zip(grid_fields, data_fields):
            arcpy.CalculateField_management(layer_name, i, '!' + j + '!', 'PYTHON')

        self.fields_names = [f.name for f in arcpy.ListFields(self.grid)]

    def tabulate_intersection(self, data_type, data_source, grid_fields, data_fields, field_types):
        """Performs tabular intersection with self.grid and the input data, data_source.

        Creates a field for each element in data_fields in self.grid ~grid_fields. Calculates the area (percentage)
        intersection and populates self.grid.

        data_type, data_source, grid_fields, data_fields, field_types are provided by a specifically formatted JSON file

        """

        # Create fields
        for field, field_type in zip(grid_fields, field_types):
            if not self.__field_exists(field):
                arcpy.AddField_management(self.grid, field, field_type)

        layer_name = 'grid_layer'
        arcpy.MakeFeatureLayer_management(self.grid, layer_name)
        table = data_type
        arcpy.TabulateIntersection_analysis(self.grid, 'GRID_ID', data_source, table)
        arcpy.AddJoin_management(layer_name, 'GRID_ID', table, 'GRID_ID')

        # Calculate fields in grid
        for i, j in zip(grid_fields, data_fields):
            arcpy.CalculateField_management(layer_name, i, '!' + j + '!', 'PYTHON')

        self.fields_names = [f.name for f in arcpy.ListFields(self.grid)]

    def populate_grid(self):
        """Uses the JSON file and populates self.grid

        Iterates through the JSON and for each dataset it selects the correct method to use in order to populate
        self.grid.

        """

        import json
        with open(self.json_data) as f:
            data = json.load(f)
            data = data['DATA']

        # Parse JSON data for use in one of the three methods
        for i in data:
            method = i['HeatMap Method']
            short_name = i['Short Name']
            data_path = i['Data Path']

            if method == 'Zonal Stats':
                self.zonal_statistics(short_name, data_path)

            elif method in ['Spatial Join', 'Tabulate Intersection']:
                data_fields = i['Fields']['Data Fields']
                grid_fields = i['Fields']['Grid Fields']
                field_types = i['Field Attributes']['Field Types']
                merge_rule = i['Field Attributes']['Merge Rule']
                join_delimiter = i['Field Attributes']['Join Delimiter']

                if method == 'Spatial Join':
                    self.spatial_join(short_name, data_path, grid_fields, data_fields, field_types, merge_rule,
                                      join_delimiter)
                else:
                    self.tabulate_intersection(short_name, data_path, grid_fields, data_fields, field_types)

            else:
                raise Exception

    def __field_exists(self, field_name):
        """Checks if field_name already exists in self.grid.

        """

        return field_name in self.fields_names
