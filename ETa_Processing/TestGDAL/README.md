
# Attempt at getting QGIS functions to work on a python script
- Need use to use GDAL to open .gdb files

## GDAL has some command line packages and a python module
  - I installed the GDAL package with cygwin on windows
  - orginfo is a command in the GDAL package
  - ```ogrinfo -al "ds2677.gdb" ```
    - Prints ALL data in the dataset
    - Can also be used on the Anaconda3(see below) command prompt if GDAL has been installed
  - ```orginfo --format```
    - Prints all formats that can be opened...
    -  OpenFileGDB -vector- (rov): ESRI FileGDB
      - This one is for .gdb

## GDAL for python3:
- Setting up environment:
  - ~~pip3 install numpy~~
    - Won't work on my environment, have to use Anaconda3
  - Install Anaconda3
  - On the anaconda3 command prompt:
    - ```conda install numpy```
    - ```conda install GDAL```
      - enter 'y'
      - some environment issues might occur but whatever
    - ```conda install -c conda-forge gdal```
      - Maybe this one too, idk?
- References:
  - https://pcjericks.github.io/py-gdalogr-cookbook/layers.html
  - https://gis.stackexchange.com/questions/32762/how-to-access-feature-classes-in-file-geodatabases-with-python-and-gdal
  - https://gdal.org/python/osgeo.ogr-module.html
- Pretty much use osgeo to read and process .gdb files and GDAL to process .tif?

## To run:
- ```python TestGDAL.py```
  - Should run on Anaconda3
  - Will need to change PathName1 to work properly


## .gdb Vector processing with ogr
- General structure:
  - Dataset(.gbd) -> Layer -> Feature -> Geometry (Vector/MultiPolygon)
- Need to reference a specific driver to open .gdb files
  -  "OpenFileGDB" is for .gdb
  - ```driver = ogr.GetDriverByName("OpenFileGDB")```
    - To get the specific driver from ogr
- Using the driver object from GetDriverByName to actually open a .gdb
  - ```DataSource = driver.Open(PathName1, 0)```
- Grab a layer from the opened database
  - ```layer = DataSource.GetLayer()```
- The layer class has lots of built in functions, see documentations...
- Here are a few useful functions examples:
  - ```featureCount = layer.GetFeatureCount()```
    - Returns an int of how many features are in the layer
  - ```layer.SetAttributeFilter("Acres > 5000")```
    - Filters the layer to only have features where the value of the column Acres is greater than 5000
    - The parameter can be SQL queries, NOTE the syntax has to be exact
  - ```layer.ResetReading()```
    - I think this just resets any filtering
  - ```for feature in layer```
    - A for loop to iterate through every feature in the layer
    - ```feature.GetField(1)```
      - To get specific column values in a feature, note OBJECTID is omitted
    - ```geom = feature.GetGeometryRef()```
      - Returns a Geometry class object, used to extract vector/polygon information
        - ```geom.ExportToJson()```
          - Returns a Json that describes the vector as a polygon, will need to convert to longitude and latitude tho...
