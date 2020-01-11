# Finds the center point of every field polygon and writes to a psql table
- Modification of ExtractVetorData.py, using ETaCrop2014.shp... will need to use the shapefiles in processed_shapes later?
- Removed the filtering option that was in ExtractVetorData.py
- Expecting a table setup in this form:
   - ```CREATE TABLE huron_delano_centers (id INT, crop VARCHAR(100), acres FLOAT, centroid JSON);```
   - The centroid json will have one entry: "Center"
    - The actual point will look like this: POINT (-120.03523115085 36.1505714767268)
