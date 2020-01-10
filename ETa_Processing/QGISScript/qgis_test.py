# filename = "\\..\\..\\Users\\richa\\Documents\\GitHub\\powwowEnergyCapstone\\QGISScript\\qgis_test.py"
 # exec(open('C:/Users/richa/Documents/GitHub/powwowEnergyCapstone/QGISScript/qgis_test.py'.encode('utf-8')).read())
#reset with
# os.system('clear')
import gdal
import processing
from qgis.PyQt.QtCore import QVariant
QgsProject.instance().clear()


# Original unaltered Crop2014 dataset:
# Crop2014Path = "\\..\\..\\Users\\richa\\Documents\\PowWowData\\landiq\\ds2677.gdb"
# Original dataset with the z dimension removed and maybe buffered...:
# Crop2014Path = "\\..\\..\\Users\\richa\\Documents\\PowWowData\\landiq\\Crop2014\\Crop2014.shp"
# Original dataset withe z-dimension removed and only fields around .tif ETa data
# Crop2014Path = "\\..\\..\\Users\\richa\\Documents\\PowWowData\\landiq\\CropCrop2014\\CropCrop2014.shp"
# Just the features in Crop2014 that touch/intersect with the .tif file
Crop2014Path = "\\..\\..\\Users\\richa\\Documents\\PowWowData\\landiq\\ETaCrop2014\\ETaCrop2014.shp"

#A temp path for some tests...
TempPath = "\\..\\..\\Users\\richa\\Documents\\PowWowData\\landiq\\Temp\\CropTemp.shp"

# Open vector layer...
# CropLayer = QgsVectorLayer(Crop2014Path, "", "ogr")
# CropLayer = iface.addVectorLayer(Crop2014Path,"" ,"ogr")
# if not CropLayer:
  # print("Layer failed to load!")

# To make a duplicate
# QgsVectorFileWriter.writeAsVectorFormat(CropLayer, TempPath, "UTF-8", driverName="ESRI Shapefile")








# # This was to polygonize a .tif... not needed anymore...
# ETaPath = "\\..\\..\\Users\\richa\\Documents\\PowWowData\\2010_2018-sample\\ETa_2010001.tif"
# ETaLayer = iface.addRasterLayer(ETaPath, "ETa Layer")
# PolyDictInput = {
# 'INPUT' : '/../../Users/richa/Documents/PowWowData/2010_2018-sample/ETa_2010001.tif',
# 'BAND' : 1,
# 'FIELD': 'VALUE',
# 'EIGHT_CONNECTEDNESS': -8,
# 'OUTPUT' : 'TEMPORARY_OUTPUT'
# }
# TifPoly = processing.run("gdal:polygonize", PolyDictInput)
# iface.addVectorLayer(TifPoly['OUTPUT'],"ETaPolygonized" ,"ogr")
#
#










#Zonal Statistics input:
# processing.algorithmHelp("qgis:zonalstatistics")
ZonalInputDict = {
"INPUT_RASTER": "",
"RASTER_BAND": 1,
# "INPUT_VECTOR": Crop2014Path,
"INPUT_VECTOR": TempPath,
"COLUMN_PREFIX": "_",
"STATS": [0,1,2,3]
}


# QgsVectorFileWriter.writeAsVectorFormat(CropLayer, TempPath, "UTF-8", driverName="ESRI Shapefile")
# TempLayer = QgsVectorLayer(TempPath, "", "ogr")
TempLayer = iface.addVectorLayer(TempPath, "", "ogr")

caps = TempLayer.dataProvider().capabilities()


#For the year 2014 .tif files range from ETa_2014001.tif to ETa_2014365.tif
for i in range(1,366):


    #Zonal Statistics Stuff:
    ETaFilePath = "\\..\\..\\Users\\richa\\Documents\\PowWowData\\2010_2018\\ETa_2014" + str(i).zfill(3) + ".tif"
    #This inputs change every .tif file...
    ZonalInputDict["INPUT_RASTER"] = ETaFilePath
    #Run zonal zonal statistics, output will be saved to vector layer
    Out = processing.run("qgis:zonalstatistics", ZonalInputDict)

    #Write output to a csv:
    ProcessedETaPath = "\\..\\..\\Users\\richa\\Documents\\PowWowData\\landiq\\ProcessedETa\\CropETa_2014" + str(i).zfill(3) + ".csv"
    #Writes to csv, some attributes are removed
    QgsVectorFileWriter.writeAsVectorFormat(TempLayer, ProcessedETaPath, "UTF-8", attributes = [0,1,2,3,11,12,13,14,15,16], driverName = "CSV")
    # QgsVectorFileWriter.writeAsVectorFormat(TempLayer, ProcessedETaPath, "UTF-8", driverName = "CSV")


    #The below section might cause bugs
    # #Remove zonal statistics field from vector layer
    if caps & QgsVectorDataProvider.DeleteAttributes:
        res = TempLayer.dataProvider().deleteAttributes([13,14,15,16])
    TempLayer.updateFields()





print("Script completed!")
