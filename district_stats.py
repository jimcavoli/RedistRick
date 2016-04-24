import arcpy
import statistics
import csv


class DistrictStats:
    def __init__(self, shapefile):
        self.shapefile = shapefile

    def summary(self, field):
        return Summary(self.shapefile, field)

    def csv(self, fields, outfile):
        with open(outfile, 'wb') as output:
            wr = csv.writer(output, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for field in fields:
                s = self.summary(field)
                wr.writerow([field, s.mean(), s.median(), s.stdev()])


class Summary:
    def __init__(self, shapefile, field):
        self.shapefile = shapefile
        self.field = field
        self.values = []
        cursor = arcpy.SearchCursor(shapefile)
        for row in cursor:
            self.values.append(float(row.getValue(field)))

    def mean(self):
        return statistics.mean(self.values)

    def median(self):
        return statistics.median(self.values)

    def stdev(self):
        return statistics.stdev(self.values)

# Example usage:
# ds = DistrictStats("C:/GIS/Project/tl_rd13_04_tract10.shp")
# print ds.summary("COUNTYFP10").stdev()
# ds.csv(["FID", "STATEFP10", "ALAND10"], "out.csv")
