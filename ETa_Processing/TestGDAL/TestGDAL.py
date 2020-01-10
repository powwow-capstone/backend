import numpy
import os
import json
from osgeo import gdal
from osgeo import ogr
import ogr, osr

#Layer -> Feature -> Feature.GetGeometryRef().ExportToJson() -> Json_Geom
# def ConvertJasonGeometry(Json_Geom):
#     try:
#         if(Json_Geom['type'] != 'MultiPolygon'):
#             print("Error, invalid json passed")
#             return
#     except:
#         print("Error, invalid json passed")
#         return
#
#
#     print("Success")
#     return 1




#This will depend on your environment
PathName1 = r"../../../PowWowData/landiq/ds2677.gdb"
PathName2 = "../../../PowWowData/2010_2018-sample/ETa_2010001.tif"  #Use for opening raster files with GDAL


#To open .gdb file...
driverName = "OpenFileGDB"
driver = ogr.GetDriverByName(driverName)
if driver is None:
    print( "%s driver not available." % driverName)
    exit()

# Open the .gbd using the appropriate driver
DataSource = driver.Open(PathName1, 0)
if DataSource is None:
    print ("Could not open dataset")
    exit()

# Dataset opened, now get layer
layer = DataSource.GetLayer()

# Apply some filtering
layer.SetAttributeFilter("Acres > 5000")


# Layer - > Feature - > Geometry

# geom_Json = OneFeature.GetGeometryRef().ExportToJson()
# geom = json.loads(geom_Json)
# print(geom["coordinates"][0][0][0][0])

# ConvertJasonGeometry(geom["coordinates"])



for feature in layer:
    print(feature.GetField("Crop2014"))
    # geom = feature.GetGeometryRef()
    # huh = geom.Centroid().ExportToWkt()
    # print(huh)
    # print(geom.ExportToWkt())
    # print(geom.CoordinateDimension())











#This is used to open .tif files?
# dataset = gdal.Open(PathName1, gdal.GA_ReadOnly)
# if not dataset:
#     print("Error!")
# else:
#     print("Success!")
