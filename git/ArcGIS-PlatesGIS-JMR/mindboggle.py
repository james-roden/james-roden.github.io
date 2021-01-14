import arcpy


south_x = 380061.32034356
north_x = 380768.427124746

west_y = 3690279
east_y = 3690986.10678119



def f(d):
    with arcpy.da.UpdateCursor(d, ['SHAPE@']) as cursor:
        for row in cursor:
            pnt = row[0].getPart()
            x = pnt.X
            y = pnt.Y
            # NE section
            if x > north_x:
                if y > east_y:
                    x += 3000
                    y += 1500
                    pnt_g = arcpy.Point(x, y)
                    row[0] = pnt_g
            # SE section
            if x > south_x:
                if y < east_y:
                    x += 3000
                    y -= 1500
                    pnt_g = arcpy.Point(x, y)
                    row[0] = pnt_g
            # SW section
            if x < south_x:
                if y < west_y:
                    x -= 3000
                    y -= 1500
                    pnt_g = arcpy.Point(x, y)
                    row[0] = pnt_g
            # NW section
            if x < north_x:
                if y > west_y:
                    x -= 3000
                    y += 1500
                    pnt_g = arcpy.Point(x, y)
                    row[0] = pnt_g

            cursor.updateRow(row)

