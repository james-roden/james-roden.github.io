# -----------------------------------------------
# Name: PlatesGIS
# Purpose: Collection of functions for rotating and moving features for paleoreconstruction
# Author: James M Roden
# github.com/GISJMR/PlatesGIS
# Created: March 2018
# ArcGIS Version: 10.5
# Python Version 2.6
# Dependencies: Numpy 1.9.3
# PEP8 & PyCharm 2016.2.2
# -----------------------------------------------

import math
import arcpy
import numpy


# Custom exception for unsupported geometry
class UnsupportedGeometry(Exception):
    pass


# Transformation function
def transformation(x, y, x_translate, y_translate, x_origin=0, y_origin=0, angle=0, units="DEGREES"):
    """
    Rotates and translates the input x and y to the location as described by the x_translate, y_translate and angle
    parameters. This is done by using the rotation matrix in 2D space and also performing a shear in 3D space --
    which casts its shadow back to 2D space as a translation.

    x: x coordinate
    y: y coordinate
    x_translate: Translation along the x-axis
    y_translate: Translation along the y-axis
    origin_x: x coordinate of origin
    origin_y: y coordinate of origin
    angle: Angle of rotation -- radians or degrees (default)
    units: Angle units -- default = "DEGREES"
    return: Tuple (x, y)
    """

    # Shift to origin (0,0)
    x -= x_origin
    y -= y_origin

    # Convert to radians
    if units == "DEGREES":
        angle = math.radians(angle)

    # Create linear transformation matrix
    transformation_matrix = numpy.matrix([[math.cos(angle), -math.sin(angle), x_translate],
                                          [math.sin(angle), math.cos(angle), y_translate]])

    # Create vertices vector
    vector = numpy.matrix([[x],
                           [y],
                           [1]])

    # Matrix-Matrix Multiplication
    output_vector = transformation_matrix * vector

    x = output_vector.item(0)  # New x coordinate
    y = output_vector.item(1)  # New y coordinate
    return x + x_origin, y + y_origin  # Shift back to original origin


# Must be supplemented with plate model feature class. See github documentation.
def plates_gis(features):
    """
    Applies rotation and translation of each feature using its corresponding attributes.

    features: Polygon, polyline or point that have been run through Intersect_analysis with custom plate model
    return: Paleo rotated version of input features
    """

    # Hard coded fields from custom plate model. See github doc for more information
    fields = ["SHAPE@", "ROTATION", "X_TRANS", "Y_TRANS", "PD_CENT_X", "PD_CENT_Y"]

    desc = arcpy.Describe(features)

    with arcpy.da.UpdateCursor(features, fields) as cursor:

        for row in cursor:
            angle = row[1]
            x_translate = row[2]
            y_translate = row[3]
            x_origin = row[4]
            y_origin = row[5]

            if desc.shapeType == "Point":
                point = row[0].getPart()
                x, y = transformation(point.X, point.Y,x_translate, y_translate, x_origin, y_origin, angle)
                point = arcpy.Point(x, y)
                point_geometry = arcpy.PointGeometry(point)
                row[0] = point_geometry
                cursor.updateRow(row)

            elif desc.shapeType in ["Polygon", "Polyline"]:
                parts = arcpy.Array()  # Holds feature part(s)
                rings = arcpy.Array()  # Holds feature ring(s)
                ring = arcpy.Array()  # Holds current ring

                for part in row[0]:

                    for point in part:
                        if point:
                            x = point.X
                            y = point.Y
                            x, y = transformation(point.X, point.Y, x_translate, y_translate, x_origin, y_origin, angle)
                            rotated_point = arcpy.Point(x, y)
                            ring.add(rotated_point)
                        else:
                            # Null means we've reached end of ring -- save it
                            rings.add(ring)
                            ring.removeAll()

                    # last ring of feature object -- save it
                    rings.add(ring)
                    ring.removeAll()

                    # Remove nesting if we only have one ring in feature
                    if len(rings) == 1:
                        rings = rings.getObject(0)

                    # Add rings to part and reset rings array for next feature
                    parts.add(rings)
                    rings.removeAll()

                # Remove nesting if we only have on part (i.e. not a multi-part feature)
                if len(parts) == 1:
                    parts = parts.getObject(0)

                # Replace geometry in-place with new geometry
                if desc.shapeType == "Polygon":
                    row[0] = arcpy.Polygon(parts, sr)
                else:
                    row[0] = arcpy.Polyline(parts, sr)
                parts.removeAll()
                cursor.updateRow(row)

            else:
                raise UnsupportedGeometry


# Find angle of rotation function
def find_rotation_angle(a, b, c):
    """
    Given three points, return the angle between a & b using the law of Cosines
    :param a: Point a (tuple)
    :param b: Point b (tuple)
    :param c: Point c (tuple)
    :return: Angle in degrees (float)
    """

    def vector_length(i, j):
        """
        Calculate the vector length between two points
        :param i: First point (tuple)
        :param j: Second point (tuple)
        :return: Vector length (float)
        """

        length = math.sqrt( ((i[0] - j[0]) ** 2) + ((i[1] - j[1]) ** 2) )
        return length

    # Calculate the three lengths of the triangle
    vector_ab = vector_length(a, b)
    vector_bc = vector_length(b, c)
    vector_ca = vector_length(c, a)

    # Use the Law of Cosines to find angle
    dividend = (vector_bc ** 2 + vector_ca ** 2) - vector_ab ** 2
    divisor = 2 * vector_ca * vector_bc
    r = dividend/divisor
    r = math.acos(r)  # Returned in radians
    return math.degrees(r)


# End of script
