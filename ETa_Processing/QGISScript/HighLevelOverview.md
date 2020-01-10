TLDR: Performing preprocessing with QGIS, a "clipped" vector shapefile was used to apply zonal statistics using 365 ETa files for the year 2014, output was exported as a csv and uploaded to the database

- The goal of this script is to preform "preprocessing" using the algorithms on QGIS, I am considering the machine learning portion as postprocessing
  - This means that this script runs on the QGIS python console
  - It might be possible to run this script outside of QGIS but setting up the environment is complicated and would not provide a visualization of the layer and will not provide a GUI on viewing data
- Eta data is provided as a .tif file with metadata included inside, crop census data is provided as a vector dataset with multiple polygons to represent fields
- Overlaying vector data and raster (.tif) and running QGIS's "zonal statistics" to calculate useful statistics like mean, median and standard deviation.
  - Vector polygons/fields that have raster data overlapping will have zonal statistics output added as a values to that feature, so in every vector there will be statistical data along with crop, acre, shape, ect.
- In this script vectors that overlapping/intersect with the raster data needed to be selected since running the zonal statistics algorithms on ALL of California's crop census polygons would take too long
  - A "clipped" shapefile for the crop census dataset was created using QGIS "polygonize" on raster data to form a vector layer, then an intersection algorithm was run between the polygonize raster layer and the crop census vector layer to determine meaningful/relevant crop census vectors
  - I did not realize that this clipped shapefile was already provided under the folder "processed_shapes"
- Since the census data was for the year 2014 only and ETa data is for 2010-2018, it will only be reasonable to perform zonal statistics for the year 2014
- In a loop for every day in the year 2014, a ETa (.tif) file is loaded and zonal statistics are run on the clipped crop census shapefile
  - Since the zonal statistics algorithm output is added to the feature table thing and the output cannot be redirected, I had to remove these values every iteration to prevent the feature table to have over 1000 values
    - Also the type of calculations for zonal statistics can be changed, I set it for Count, Sum, Mean and Median... but more are possible
  - Once completed, the feature table is exported as a csv, I also removed some useless data such as comments, and source info
- Processing with every 2014 ETa file took about 30 minutes
- I then manually upload these csv files to the database outside of this script
  - Note: it was not uploaded to PSQL database, no table has been made yet
