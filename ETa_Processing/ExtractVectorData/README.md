# Python script to extract polygons from a vector shape file
- Results are placed in a psql table

 
## To run:
- NOTE: A psql table needs to be set up before this script is run
  - The INSERT command needs to be updated too, specifically the ```cur.execute``` function
- Needed to install psycopg2:
  - ```conda install -c anaconda psycopg2```
- ```python ExtractVetorData.py [FilePath] [Filter]```
- FilePath is to a .shp or a .gdb file
  - NOTE: .shp files should have their Z dimension removed!!
- Filter is in SQL format
- You will also need a 'database.ini' file in order to connect the psql database  
- Some examples:
  - ```python ExtractVetorData.py "../../../PowWowData/landiq/ETaCrop2014/ETaCrop2014.shp"```
  - ```python ExtractVetorData.py "../../../PowWowData/landiq/ds2677.gdb"```
  - ```python ExtractVetorData.py "../../../PowWowData/landiq/ds2677.gdb" "County = 'Santa Barbara' AND Acres < 0.05"```
