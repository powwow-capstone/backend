TLDR: To get coordinate data the .gdb Dataset was opened with ogr, a class was returned with this structure: DataSource->Layer->Feature->Geometry->Individual polygon information, polygon coordinate system was converted from EPSG3310 to EPSG4326, data was formatted and uploaded to our PSQL server

- The goal of this script is to extract the coordinate information on individual polygons
- Vector data was provided to us as a .gdb file which contains shapefiles that describe the individual polygons for around 300,000 different fields.
- Along with this polygon data was information on crop, acres and county
- To open the .gdb file a python module "ogr" was used
  - A specific driver called "OpenFileGDB" was selected from the "ogr"
  - This driver is used to open/read the .gdb file
- Opening the file returns a "DataSource" class
- From that "DataSource" class a "Layer" class can then extracted
- The "Layer" class contains multiple "Feature" classes (the individual polygon/field/crop data is in the class)
- Before using the Layer class it was filtered using SQL commands
  - Currently it was set to filter for only Santa Barbara county polygons
- Individual Features in the Layer were accessed in a for loop to get "Geometry" class
  - The coordinates were extracted from every Geometry class as a json
    - The coordinates were returned in EPSG3310, EPSG4326(longitude and latitude) was desired
    - The python module "osr" was used for conversion
  - Converted coordinates were formated then uploaded to our PSQL database using "psycopg2"
