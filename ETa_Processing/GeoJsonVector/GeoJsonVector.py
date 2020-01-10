import ogr, osr
import json
import os
import psycopg2
from psycopg2 import sql
import getpass
from configparser import ConfigParser
import sys



#Taken from: http://www.postgresqltutorial.com/postgresql-python/connect/
def config(filename='database.ini', section='postgresql'):


    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db #Returns a dictionary  with the config info for the psql database

def ConnectToDatabaseServer():
    try:
        #Read the info in the database.ini to connect to the server
        ConfigInfo = config()
        print("Attemping to connect...")
        Connection =psycopg2.connect(**ConfigInfo)
        print("Connection successful...")

        #Somthing cursor... its used to navigate the psql server
        return Connection
        # cur = Connection.cursor()

    except(Exception, psycopg2.DatabaseError) as error:
        print("Connection error:")
        print(error)

#PSQL preparation:
# Make sure you have a "database.ini" file in you working directory
# Also make sure your table as been set up in this format
# ```CREATE TABLE sbvectors2 (id INT, crop VARCHAR(100), acres FLOAT, coordinates JSON);```

#**********IMPORTANT**********
#**********IMPORTANT**********
#**********IMPORTANT**********
#MAKE SURE THE cur.execute IS INSERTING TO THE CORRECT TABLE!!!!!!

# Syntax:
# python GeoJsonVector.py [FilePath] [Filter]

#Enter any filtering as an SQL command, ex "County = 'Santa Barbara' AND Acres < 0.05"
# Some Filters:
# "Acres < 0.9"
# "County = 'Santa Barbara' AND Acres < 0.05"
# "County = 'Santa Barbara'"
# "County = 'Fresno'"

#Typical commands...
# python GeoJsonVector.py "../../../PowWowData/landiq/ETaCrop2014/ETaCrop2014.shp" "Acres < 0.52"


assert (len(sys.argv) > 1), "Need to specify file"

#Determine file extension
FileType = ""
for j in range(3,0,-1):
    FileType = FileType + sys.argv[1][len(sys.argv[1])-j]
FileType = FileType.upper()
SHP = False
GDB = False
if(FileType == "SHP"):
    print("File Format: .shp" )
    SHP = True
elif(FileType == "GDB"):
    print("File Format: .gdb" )
    GDB = True
PathName = sys.argv[1]
assert (SHP != GDB), "Invalid file format"

#Get filter
Filter = ""
if(len(sys.argv) > 2):
    Filter = sys.argv[2]

#Get driver to open file
driverName = ""
if(SHP == True):
    driverName = "ESRI Shapefile"
elif(GDB == True):
    driverName = "OpenFileGDB"
driver = ogr.GetDriverByName(driverName)
assert (driver != None), "Driver not found for some reason"


DataSource = driver.Open(PathName, 0)
assert (DataSource != None), "Could not open dataset, not found"
print("Dataset opened")

#Extract layer from dataset
Layer = DataSource.GetLayer()

#Filter the layer read from the dataset
print("Applying filter...")
Layer.SetAttributeFilter(Filter)

#Get the conversion from EPSG3310 to EPSG4326 (longitude and latitude)
inputEPSG = 3310
inSpatialRef = osr.SpatialReference()
inSpatialRef.ImportFromEPSG(inputEPSG)
outputEPSG = 4326 #For longitude and latitude
outSpatialRef = osr.SpatialReference()
outSpatialRef.ImportFromEPSG(outputEPSG)
CoorTrans = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)


# Connect to psql server
# Check that a "database.ini" file can be read
assert os.path.isfile('database.ini'), "Could not open 'database.ini'"
# Conn = ConnectToDatabaseServer()
# cur = Conn.cursor()

IndexNumber = 0
Acres = 0.0
Crop = ""

g = input("Confirm this script is writing to the correct PSQL table (y/n):")
if (g.upper() != "Y"):
    print("Now exiting...")
    exit()


print("Cycling through features...")
CurrentVector = 1;
for Feature in Layer:

    #Get Geometry/polygon data from the current feature
    Geometry = Feature.GetGeometryRef()
    #Transform to EPSG4326
    Geometry.Transform(CoorTrans)
    #Convert Geometry into a workabale json/dictionary
    GeometryJson = json.loads(Geometry.ExportToJson())
    #Remove z-axis and create a new json/dictionary

    # print(type(GeometryJson))
    with open('result.json', 'w') as fp:
        json.dump(GeometryJson, fp)


    #Insert to the psql database
    #IMPORTANT!
    #MAKE SURE YOU'RE WRITING TO THE CORRECT TABLE
    # cur.execute("""INSERT INTO huron_delano_vectors ( id, crop, acres, coordinates ) VALUES (%s, %s, %s, %s) """, (IndexNumber, Crop, Acres, json.dumps(CoorJson)))
    # cur.execute("""INSERT INTO sbvectors2 ( id, crop, acres, coordinates ) VALUES (%s, %s, %s, %s) """, (IndexNumber, Crop, Acres, json.dumps(CoorJson)))




#Commit and close connections
print("Script completed and entries placed in PSQL table")
# cur.close()
# Conn.commit()
# Conn.close()
