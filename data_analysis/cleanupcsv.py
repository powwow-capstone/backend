import csv

with open("../data/CropCensus_withETa_and_XY.csv") as in_file:
    with open("../data/CropCensus_withETa_and_XY_cleaned.csv", 'w') as out_file:
        writer = csv.writer(out_file)
        for row in csv.reader(in_file):
            if row[15]:
                writer.writerow(row)