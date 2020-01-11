# Python script to extract polygons from a vector shape file
- Results are placed in an already created PSQL table


## To run:
- NOTE: A psql table needs to be set up before this script is run
  - The INSERT command needs to be updated too, specifically the ```cur.execute``` function
- I had to use Anaconda
- Needed to install psycopg2:
  - ```conda install -c anaconda psycopg2```
- ```python ExtractVetorData.py [FilePath] [Filter]```
- FilePath is to a .shp or a .gdb file
  - NOTE: .shp files should have their Z dimension removed!!
  - Note that ETaCrop2014.shp was used for previous polygons but should be replace by
- Filter is in SQL format
- You will also need a 'database.ini' file in order to connect the psql database  
- Some examples:
  - ```python ExtractVetorData.py "../../../PowWowData/landiq/ETaCrop2014/ETaCrop2014.shp"```
  - ```python ExtractVetorData.py "../../../PowWowData/landiq/ds2677.gdb"```
  - ```python ExtractVetorData.py "../../../PowWowData/landiq/ds2677.gdb" "County = 'Santa Barbara' AND Acres < 0.05"```

## Some notes
- The PSQL table sbvectors was likely written using ds2677.gdb which was a bit buggy with a z dimension
- sbvectors2 might have also been written using ds2677.gdb
- The table huron_delano_vectors was definitely done using a shape file called ETaCrop2014.shp which is a "cleaned" version of ds2677.gdb
  - It only includes Huron and Delano fields that intersect with ETa.tif locations  
  - The z dimension was removed and a buffer operation was applied using QGIS to solve some bugs
  - This shapefile mostly works but has a few buggy fields
  - The shapefile has been copied to the Ubuntu server and is under data/PowWowETa2019/ETaCrop2014/
  - I later discovered there already existed individual shapefiles for Huron and Delano under the folder processed_shapes...
    - TODO rebuild the table huron_delano_vectors using these existing shape files.
    - ```python ExtractVetorData.py "../../../PowWowData/processed_shapes/Del_32611_30meterbuffer_clean.shp"```
